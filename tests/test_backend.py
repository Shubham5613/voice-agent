"""Backend guard tests: run with `.venv/bin/python -m pytest tests/test_backend.py -q`.
They exercise the real FastAPI app in-process against a throwaway SQLite file (AGENT_DB_PATH), never the demo calls.db.
Simulations cannot cover these: ElevenLabs simulations never execute webhook tools."""
import os, sys, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
os.environ.setdefault("ELEVENLABS_API_KEY", "test")
import tempfile
os.environ["AGENT_DB_PATH"] = os.path.join(tempfile.mkdtemp(prefix="agent-test-"), "test.db")  # keep test events out of the demo database
from fastapi.testclient import TestClient
from backend.main import app
from backend.personalise import value_line, personal_context, compose_hook, rupees_in_words, fee_outlook, offer_validity
from backend.main import CARDS

c = TestClient(app)
ref = lambda tag: f"test-{tag}-{time.time_ns()}"


def post(path, **body):
    r = c.post(path, json=body)
    assert r.status_code == 200, r.text
    return r.json()


# ---------- personalisation ----------
def test_rupees_in_words_indian_style():
    assert rupees_in_words(6500) == "six thousand five hundred"
    assert rupees_in_words(125000) == "one lakh twenty-five thousand"


def test_value_line_speaks_categories_not_amounts():
    lead = {"customer_name": "Priya", "relationship": "existing", "spend_hint": "flights and hotels", "spend_label": "travel",
            "monthly_category_spend_inr": 35000}
    line = value_line("regalia_gold", lead)
    assert line.startswith("Going by your travel spends with us, that's roughly")
    assert "35" not in line and "thirty-five" not in line          # the spend figure itself is never spoken
    assert "lounge" in line


def test_value_line_empty_without_spend_band():
    assert value_line("moneyback_plus", {"relationship": "new", "customer_name": "Vikram"}) == ""


def test_new_lead_is_personalised_only_by_source():
    lead = {"customer_name": "Rahul", "relationship": "new", "lead_source": "you'd tapped the card offer inside the Swiggy app last week"}
    assert "no bank data" in personal_context(lead) or "lead source" in personal_context(lead)
    hook = compose_hook("You've been shortlisted for a card.", lead)
    assert hook.startswith("You'd tapped the card offer") and "you've been shortlisted" in hook


# ---------- eligibility ----------
def test_pre_approved_existing_customer_needs_no_questions():
    r = post("/tools/check_eligibility", lead_id="L002", card_id="regalia_gold")
    assert r["status"] == "eligible" and r["basis"] == "pre_approved_on_bank_record"


def test_new_lead_without_details_is_asked_not_rejected():
    r = post("/tools/check_eligibility", lead_id="L006", card_id="millennia")
    assert r["status"] == "need_details"


def test_new_lead_with_details_is_scored():
    r = post("/tools/check_eligibility", lead_id="L006", card_id="millennia", age=30, employment_type="salaried", monthly_income_inr=60000)
    assert r["status"] == "eligible"
    r = post("/tools/check_eligibility", lead_id="L006", card_id="regalia_gold", age=30, employment_type="salaried", monthly_income_inr=60000)
    assert r["status"] == "ineligible" and r["alternative_card"]


# ---------- link: the four guards ----------
def test_link_requires_eligibility_for_new_lead():
    # L005 (Vikram) has had no eligibility check in this process unless another test ran one; use a card nobody checks.
    r = post("/tools/send_application_link", lead_id="L005", card_id="swiggy_hdfc", phone_last4="1098", channel="whatsapp",
             customer_said_yes_after_disclosure=True, call_ref=ref("elig"))
    assert r["status"] == "eligibility_required"


def test_link_is_two_phase_disclosure_then_send():
    cr = ref("twophase")
    first = post("/tools/send_application_link", lead_id="L004", card_id="millennia", phone_last4="2109", channel="whatsapp", call_ref=cr)
    assert first["status"] == "disclosure_required"
    assert first["say_exactly"].startswith("Quick formality before I send it: the annual fee is one thousand rupees")
    assert "subject to the bank's eligibility check. Shall I go ahead?" in first["say_exactly"]
    second = post("/tools/send_application_link", lead_id="L004", card_id="millennia", phone_last4="2109", channel="whatsapp",
                  call_ref=cr, customer_said_yes_after_disclosure=True)
    assert second["status"] == "sent" and second["reference"].startswith("APP-")


def test_link_only_to_registered_number():
    r = post("/tools/send_application_link", lead_id="L004", card_id="millennia", phone_last4="9999", channel="whatsapp",
             call_ref=ref("mismatch"), customer_said_yes_after_disclosure=True)
    assert r["status"] == "mismatch"


def test_link_idempotent_within_one_call_but_not_across_calls():
    cr = ref("idem")
    a = post("/tools/send_application_link", lead_id="L002", card_id="regalia_gold", phone_last4="5678", channel="whatsapp",
             call_ref=cr, customer_said_yes_after_disclosure=True)
    b = post("/tools/send_application_link", lead_id="L002", card_id="regalia_gold", phone_last4="5678", channel="whatsapp",
             call_ref=cr, customer_said_yes_after_disclosure=True)
    assert a["status"] == "sent" and b["status"] == "already_sent" and b["reference"] == a["reference"]
    other = post("/tools/send_application_link", lead_id="L002", card_id="regalia_gold", phone_last4="5678", channel="whatsapp",
                 call_ref=ref("idem2"), customer_said_yes_after_disclosure=True)
    assert other["status"] == "sent" and other["reference"] != a["reference"]


# ---------- leads API ----------
def test_leads_api_carries_personalisation():
    leads = {l["lead_id"]: l for l in c.get("/api/leads").json()}
    assert leads["L002"]["value_line"] and "banked with us" in leads["L002"]["personal_context"]
    assert leads["L005"]["value_line"] == ""   # minimal-data lead still works


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-q"]))


def test_fee_outlook_is_honest_both_ways():
    priya = {"relationship": "existing", "spend_label": "travel", "monthly_category_spend_inr": 35000}   # 4.2L/yr >= 4L waiver
    out = fee_outlook(CARDS["regalia_gold"], priya)
    assert out.startswith("It's a paid card") and "you'd likely cross it" in out and "voucher, not a refund" in out
    for banned in ("lifetime", "effectively", "free"):
        assert banned not in out.lower()
    rahul = {"relationship": "new", "spend_label": "food-delivery", "monthly_category_spend_inr": 8000}  # 96k/yr < 2L waiver
    out = fee_outlook(CARDS["swiggy_hdfc"], rahul)
    assert "may not get there" in out and "voucher" not in out
    assert fee_outlook(CARDS["moneyback_plus"], {"relationship": "new"}).startswith("It's a paid card")


def test_offer_validity_only_for_existing():
    assert "thirtieth of November" in offer_validity({"relationship": "existing", "offer_valid_till": "the thirtieth of November"})
    assert offer_validity({"relationship": "new", "offer_valid_till": "the thirtieth of November"}) == ""


def test_send_summary_logs_without_last4():
    r = post("/tools/send_summary", lead_id="L002", card_id="regalia_gold", call_ref=ref("sum"), customer_said_yes=True)
    assert r["status"] == "sent"
    kinds = [e["kind"] for e in c.get("/api/events", params={"lead_id": "L002"}).json()]
    assert "summary_sent" in kinds


def test_limit_line_only_for_pre_approved_existing():
    from backend.personalise import limit_line
    assert "three lakh" in limit_line({"relationship": "existing", "pre_approved_limit_inr": 300000})
    assert limit_line({"relationship": "new", "pre_approved_limit_inr": 300000}) == ""


def test_whatsapp_intro_flag_sets_intro_line_and_logs(monkeypatch):
    import backend.main as m
    class FakeResp:
        status_code = 200
        def json(self): return {"signed_url": "wss://test"}
    class FakeCx:
        async def __aenter__(self): return self
        async def __aexit__(self, *a): return False
        async def get(self, *a, **k): return FakeResp()
    monkeypatch.setattr(m.httpx, "AsyncClient", lambda **k: FakeCx())
    monkeypatch.setattr(m, "agent_id", lambda: "agent_test")
    r = c.get("/api/session", params={"lead_id": "L004", "force": 1, "intro": 1}).json()
    assert r["dynamic_variables"]["intro_line"].startswith("I sent you a short WhatsApp")
    kinds = [e["kind"] for e in c.get("/api/events", params={"lead_id": "L004"}).json()]
    assert "whatsapp_intro_sent" in kinds


def test_reason_first_opener_holds_product_until_permission(monkeypatch):
    import backend.main as m
    class FakeResp:
        status_code = 200
        def json(self): return {"signed_url": "wss://test"}
    class FakeCx:
        async def __aenter__(self): return self
        async def __aexit__(self, *a): return False
        async def get(self, *a, **k): return FakeResp()
    monkeypatch.setattr(m.httpx, "AsyncClient", lambda **k: FakeCx())
    monkeypatch.setattr(m, "agent_id", lambda: "agent_test")
    # existing: no card name, no 'credit card', no percentages in turn 1; value + card + 'the catch' in turn 2
    d = c.get("/api/session", params={"lead_id": "L002", "force": 1}).json()["dynamic_variables"]
    assert d["opener_style"] == "reason_first"
    t1 = d["opener_turn1"].lower()
    assert t1.startswith("hi priya.") and "regalia" not in t1 and "credit card" not in t1 and "percent" not in t1
    assert t1.endswith("thirty seconds to check if it's actually useful?")
    assert "Regalia Gold" in d["opener_turn2"] and "the catch" in d["opener_turn2"]
    # new with source: the source is the reason; turn 2 is an either-or question
    d = c.get("/api/session", params={"lead_id": "L001", "force": 1}).json()["dynamic_variables"]
    assert "You'd tapped the card offer inside the Swiggy app" in d["opener_turn1"] and d["opener_turn2"].startswith("Quick one:")
    # tier 0 lead: no product in turn 1, full spend menu in turn 2, reveal chosen by the answer (UPI -> RuPay card)
    d = c.get("/api/session", params={"lead_id": "L005", "force": 1}).json()["dynamic_variables"]
    t1 = d["opener_turn1"].lower()
    assert "card" not in t1 and "pre-approved" not in t1 and "list" not in t1 and t1.endswith("got thirty seconds?")
    assert all(w in d["opener_turn2"] for w in ("UPI", "groceries and fuel", "online shopping", "travel"))
    assert "card id upi_rupay" in d["opener_benefit"] and "card id regalia_gold" in d["opener_benefit"]
    assert "lifetime" not in d["opener_benefit"].lower() and "free card" not in d["opener_benefit"].lower()
    # variant A still produces the old opener and no reason-first turns
    d = c.get("/api/session", params={"lead_id": "L002", "force": 1, "variant": "A_benefit"}).json()["dynamic_variables"]
    assert d["opener_style"] == "benefit_first" and d["opener_turn1"] == ""


def test_decline_promise_is_kept_by_the_dialer(monkeypatch):
    import backend.main as m, backend.db as db
    db.clear_declines("L006")
    r = post("/tools/mark_declined", lead_id="L006", card_id="millennia", reason="has better card")
    assert r["status"] == "marked"
    class FakeResp:
        status_code = 200
        def json(self): return {"signed_url": "wss://test"}
    class FakeCx:
        async def __aenter__(self): return self
        async def __aexit__(self, *a): return False
        async def get(self, *a, **k): return FakeResp()
    monkeypatch.setattr(m.httpx, "AsyncClient", lambda **k: FakeCx())
    monkeypatch.setattr(m, "agent_id", lambda: "agent_test")
    blocked = c.get("/api/session", params={"lead_id": "L006"})
    assert blocked.status_code == 409 and "declined" in blocked.json()["detail"]
    assert c.get("/api/session", params={"lead_id": "L006", "force": 1}).status_code == 200
    leads = {l["lead_id"]: l for l in c.get("/api/leads").json()}
    assert leads["L006"]["declined"] and not leads["L006"]["dnc"]   # declined is not do-not-call
    c.post("/api/dnc/clear", params={"lead_id": "L006"})
    assert not {l["lead_id"]: l for l in c.get("/api/leads").json()}["L006"]["declined"]


def test_upi_rupay_card_in_catalogue_and_eligibility():
    from backend.main import CARDS
    from backend.personalise import fee_outlook
    card = CARDS["upi_rupay"]
    assert card["annual_fee_inr"] == 250 and card["fee_waiver_spend_inr"] == 25000
    fo = fee_outlook(card, {"relationship": "new"}).lower()
    assert "paid card" in fo and "two hundred fifty" in fo and "free" not in fo
    r = c.post("/tools/check_eligibility", json={"lead_id": "L005", "card_id": "upi_rupay", "age": 38, "employment_type": "salaried", "monthly_income_inr": 45000, "call_ref": "t-upi"}).json()
    assert r["status"] == "eligible"


def test_parked_summary_logs_resume_and_is_not_a_decline():
    r = c.post("/tools/send_summary", json={"lead_id": "L002", "card_id": "regalia_gold", "context": "parked", "call_ref": ref("park"), "customer_said_yes": True}).json()
    assert r["status"] == "sent" and "talk-to-us" in r["message_for_agent"]
    ev = c.get("/api/events", params={"lead_id": "L002"}).json()
    kinds = [e["kind"] for e in ev]
    assert "parked_whatsapp" in kinds and "declined" not in kinds
    sent = [e for e in ev if e["kind"] == "summary_sent"][0]["payload"]
    assert sent["context"] == "parked" and sent["resume_link"].endswith("/resume/L002")
    # a new lead gets no resume button
    r2 = c.post("/tools/send_summary", json={"lead_id": "L005", "card_id": "upi_rupay", "context": "busy", "call_ref": ref("busy"), "customer_said_yes": True}).json()
    assert "talk-to-us" not in r2["message_for_agent"]


def test_summary_and_callback_need_consent_and_a_real_time():
    # summary without a yes: held, question returned, nothing logged as sent
    r = post("/tools/send_summary", lead_id="L001", card_id="swiggy_hdfc", context="busy", call_ref=ref("hold"))
    assert r["status"] == "confirm_required" and r["say_exactly"].startswith("Shall I WhatsApp")
    kinds = [e["kind"] for e in c.get("/api/events", params={"lead_id": "L001"}).json()]
    assert "summary_held" in kinds and kinds.count("summary_sent") == 0
    # callback with 'later' (the real Rahul call) is refused even with a yes; 'tomorrow 6 pm' is booked
    r = post("/tools/schedule_callback", lead_id="L001", when_text="later", customer_said_yes=True, call_ref=ref("cb1"))
    assert r["status"] == "need_time" and "When's a good time" in r["say_exactly"]
    r = post("/tools/schedule_callback", lead_id="L001", when_text="tomorrow 6 pm", customer_said_yes=False, call_ref=ref("cb2"))
    assert r["status"] == "need_time"
    r = post("/tools/schedule_callback", lead_id="L001", when_text="tomorrow 6 pm", customer_said_yes=True, call_ref=ref("cb3"))
    assert r["status"] == "booked"
    kinds = [e["kind"] for e in c.get("/api/events", params={"lead_id": "L001"}).json()]
    assert kinds.count("callback_booked") == 1 and kinds.count("callback_held") == 2

import re
"""Backend for the Karta credit-card voice agent.

- Serves the browser dialer (web/)
- Pre-call gate + signed session URL for ElevenLabs
- Webhook tools the agent calls (eligibility, link, callback, DNC, human, event log)
- Post-call webhook from ElevenLabs
Run:  uvicorn backend.main:app --reload --port 8000
"""
import json, os, pathlib, hashlib, datetime as dt, zoneinfo
from typing import Literal
import httpx
from backend.personalise import value_line, personal_context, compose_hook, fee_outlook, offer_validity, limit_line
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from . import db

ROOT = pathlib.Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
IST = zoneinfo.ZoneInfo("Asia/Kolkata")

LEADS = {l["lead_id"]: l for l in json.loads((ROOT / "data" / "leads.json").read_text())}
CATALOG = json.loads((ROOT / "agent" / "card_catalog.json").read_text())
CARDS = {c["id"]: c for c in CATALOG["cards"]}
OPENERS = json.loads((ROOT / "agent" / "openers.json").read_text())

app = FastAPI(title="Karta card agent backend")
app.mount("/static", StaticFiles(directory=ROOT / "web"), name="static")


def agent_id() -> str:
    st = ROOT / "agent" / ".agent_state.json"
    if os.environ.get("ELEVEN_AGENT_ID"):
        return os.environ["ELEVEN_AGENT_ID"]
    if st.exists():
        return json.loads(st.read_text()).get("agent_id", "")
    return ""


# ---------- dialer ----------
@app.get("/")
def index():
    return FileResponse(ROOT / "web" / "index.html")


@app.get("/api/leads")
def leads():
    return [l | {"dnc": db.is_dnc(l["lead_id"]), "declined": db.declined(l["lead_id"], l["offer_card_id"]), "offer_card_name": CARDS[l["offer_card_id"]]["name"],
                 "value_line": value_line(l["offer_card_id"], l), "personal_context": personal_context(l)} for l in LEADS.values()]


@app.get("/api/session")
async def session(lead_id: str, variant: str = "D_reason_first", force: int = 0, intro: int = 0):
    """Pre-call gate, then a signed URL + the dynamic variables the dialer must pass to startSession."""
    lead = LEADS.get(lead_id)
    if not lead:
        raise HTTPException(404, "unknown lead")
    if db.is_dnc(lead_id) and not force:
        raise HTTPException(409, "Lead is on the do-not-call list")
    card_for_gate = CARDS.get(lead.get("offer_card_id"), CARDS["moneyback_plus"])
    dec = db.declined(lead_id, card_for_gate["id"])
    if dec and not force:
        # The agent promised "you won't hear about this card again". The system keeps that promise.
        raise HTTPException(409, f"Customer declined {card_for_gate['name']} on {dec['ts'][:10]} and was promised no further calls about it. Pass force=1 for a demo.")
    hour = dt.datetime.now(IST).hour
    if not (10 <= hour < 19) and not force:
        # RBI Credit Card and Debit Card Directions 2025, para 11(9): representatives may contact customers only 10:00-19:00.
        raise HTTPException(409, f"Outside RBI calling window 10:00-19:00 IST (now {hour}:00 IST). Pass force=1 for a demo.")
    aid = agent_id()
    if not aid:
        raise HTTPException(500, "Agent not deployed: run python agent/deploy_agent.py")
    async with httpx.AsyncClient(timeout=20) as cx:
        r = await cx.get("https://api.elevenlabs.io/v1/convai/conversation/get-signed-url",
                         params={"agent_id": aid}, headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"]})
    if r.status_code >= 400:
        raise HTTPException(502, f"ElevenLabs: {r.text}")
    # Minimal-data principle: only lead_id, customer_name and phone are required; everything else has a default.
    card = CARDS.get(lead.get("offer_card_id"), CARDS["moneyback_plus"])
    existing = lead.get("relationship", "new") == "existing"
    if existing:
        hook = OPENERS["existing_customer"][card["id"]]
    else:
        hook = compose_hook(OPENERS["variants"].get(variant, OPENERS["variants"]["A_benefit"])[card["id"]], lead)
    # Variant D, reason-first: identity -> reason specific to them -> thirty-second ask; product only after permission.
    intro_line = "I sent you a short WhatsApp about this a minute ago. " if intro else ""
    rf = OPENERS["reason_first"]
    kind = "existing" if existing else ("new_with_source" if lead.get("lead_source") else "new_minimal")
    src = lead.get("lead_source", "")
    fill = {"customer_name": lead["customer_name"], "agent_name": "Aanya", "bank_name": "HDFC Bank", "intro_line": intro_line,
            "lead_source_cap": (src[0].upper() + src[1:]) if src else "", "value_line": value_line(card["id"], lead),
            "offer_card_name": card["name"]}
    opener_turn1 = rf["turn1"][kind].format(**fill)
    if existing:
        opener_turn2, opener_benefit = rf["after_yes_existing"].format(**fill).strip(), rf["benefit_by_answer"][card["id"]]
    elif kind == "new_minimal":
        opener_turn2 = rf["menu_minimal"]
        opener_benefit = "\n".join(f'- they said {r["answer"]} -> card id {r["card_id"] or "none"}: "{r["line"]}"' for r in rf["reveal_minimal"])
    else:
        opener_turn2, opener_benefit = rf["either_or"][card["id"]], rf["benefit_by_answer"][card["id"]]
    reason_first = variant == "D_reason_first"
    dyn = {"agent_name": "Aanya", "bank_name": "HDFC Bank", "customer_name": lead["customer_name"],
           "city": lead.get("city", "your city"), "lead_id": lead_id,
           "spend_hint": lead.get("spend_hint", "everyday spends"), "offer_card_name": card["name"], "offer_hook": hook,
           "relationship": "existing customer of the bank with a pre-approved offer" if existing else "new to the bank, on a pre-qualified list",
           "value_line": value_line(card["id"], lead), "personal_context": personal_context(lead),
           "fee_outlook": fee_outlook(card, lead), "offer_validity": offer_validity(lead), "limit_line": limit_line(lead),
           # WhatsApp-first warm-up (Callyzer playbook): a two-line intro goes out before the call so the opener is a follow-up, not a cold call.
           "intro_line": intro_line,
           "opener_style": "reason_first" if reason_first else "benefit_first",
           "opener_turn1": opener_turn1 if reason_first else "", "opener_turn2": opener_turn2 if reason_first else "",
           "opener_benefit": opener_benefit if reason_first else "",
           "call_ref": f"{lead_id}-{int(dt.datetime.now().timestamp())}"}
    if intro:
        # Real integration point: WhatsApp Business template from the bank's verified account, e.g.
        # "Hi {name}, Aanya from HDFC Bank's card team. You have a {card} offer on your account (see the HDFC app). May I call you for two minutes?"
        db.log(lead_id, "whatsapp_intro_sent", {"card_id": card["id"], "to": "number on file ending " + lead["phone"][-4:]})
    db.log(lead_id, "call_started", {"variant": variant if reason_first else ("existing_customer" if existing else variant),
                                     "offer_card_id": card["id"], "whatsapp_intro": bool(intro)})
    return {"signed_url": r.json()["signed_url"], "dynamic_variables": dyn,
            "language": lead.get("language_pref", "en"),
            "first_message": OPENERS["first_message"].get(lead.get("language_pref", "en"))}


@app.get("/api/events")
def get_events(lead_id: str | None = None):
    return db.events(lead_id)


@app.get("/api/calls")
def get_calls():
    return db.calls()


@app.post("/api/dnc/clear")
def clear_dnc(lead_id: str):
    db.remove_dnc(lead_id)
    db.clear_declines(lead_id)
    return {"ok": True}


# ---------- tools called by the agent ----------
class LogEvent(BaseModel):
    lead_id: str
    stage: Literal["OPEN", "EARLY_NO", "DISCOVER", "PITCH", "OBJECTIONS", "QUALIFY", "CLOSE", "WRAP"]
    note: str = ""


@app.post("/tools/log_event")
def tool_log_event(b: LogEvent):
    db.log(b.lead_id, "stage", b.model_dump())
    return {"ok": True}


class Eligibility(BaseModel):
    lead_id: str
    age: int | None = Field(default=None, ge=0, le=120)
    employment_type: str | None = None
    monthly_income_inr: int | None = Field(default=None, ge=0)
    city: str = ""
    card_id: str


@app.post("/tools/check_eligibility")
def tool_check_eligibility(b: Eligibility):
    card = CARDS.get(b.card_id)
    if not card:
        return {"status": "error", "message_for_agent": "That card id is not in the catalogue. Use one of: " + ", ".join(CARDS)}
    lead = LEADS.get(b.lead_id, {})
    # Existing customer with a pre-approved offer on THIS card: the bank already holds age, income and KYC.
    # Asking again is both pointless and a known drop-off point, so the check passes on the bank's record.
    if lead.get("relationship") == "existing" and lead.get("offer_card_id") == b.card_id:
        db.log(b.lead_id, "eligibility", {"card_id": b.card_id, "status": "pre_approved", "source": "bank record"})
        return {"status": "eligible", "basis": "pre_approved_on_bank_record",
                "message_for_agent": "Pre-approved on the bank's record. Do not ask age or income. Go straight to the fee disclosure (Turn A) and ask for the yes."}
    if b.age is None or b.monthly_income_inr is None or not b.employment_type:
        return {"status": "need_details",
                "message_for_agent": "This customer is not pre-approved for this card. Ask, in one question, their age and roughly their monthly income, salaried or self-employed, then call check_eligibility again with those."}
    e = card["eligibility"]
    emp = "self_employed" if "self" in b.employment_type.lower() else "salaried"
    reasons = []
    if not (e["age_min"] <= b.age <= e["age_max"]):
        reasons.append(f"age must be between {e['age_min']} and {e['age_max']}")
    annual = b.monthly_income_inr * 12
    need = e["min_monthly_income_salaried_inr"] if emp == "salaried" else e["min_annual_itr_self_employed_inr"] // 12
    if b.monthly_income_inr < need * 0.8:
        reasons.append(f"income below the minimum of about {need} rupees a month")
        status = "ineligible"
    elif b.monthly_income_inr < need:
        status = "borderline"
    else:
        status = "eligible"
    if reasons and any("age" in r for r in reasons):
        status = "ineligible"
    # suggest a lower-tier card if ineligible on income
    alt = None
    if status != "eligible":
        for c in sorted(CATALOG["cards"], key=lambda c: c["eligibility"]["min_monthly_income_salaried_inr"]):
            ce = c["eligibility"]
            if ce["age_min"] <= b.age <= ce["age_max"] and b.monthly_income_inr >= ce["min_monthly_income_salaried_inr"]:
                alt = c["name"]; break
    msg = {"eligible": "Customer qualifies to apply. You may offer to send the link after the fee disclosure.",
           "borderline": "Income is slightly under the usual minimum. Say final approval is the bank's decision; you may still send the link.",
           "ineligible": "Not eligible for this card: " + "; ".join(reasons) + (f". A possible alternative is {alt}." if alt else ". Do not promise an alternative.")}[status]
    out = {"status": status, "reasons": reasons, "alternative_card": alt, "message_for_agent": msg}
    db.log(b.lead_id, "eligibility", b.model_dump() | out)
    return out


class SendLink(BaseModel):
    lead_id: str
    card_id: str
    phone_last4: str = Field(min_length=4, max_length=4, pattern=r"^\d{4}$")
    channel: Literal["whatsapp", "sms"] = "whatsapp"
    customer_said_yes_after_disclosure: bool = False
    call_ref: str = ""


def _rupees(n: int) -> str:
    from backend.personalise import rupees_in_words
    return rupees_in_words(int(n)) + " rupees"


def disclosure_sentence(card: dict) -> str:
    """The compulsory pre-link disclosure, built from the catalogue so the agent cannot misquote it."""
    return (f"Quick formality before I send it: the annual fee is {_rupees(card['annual_fee_inr'])}, "
            f"{card['fee_waiver'][0].lower() + card['fee_waiver'][1:]}, and approval is subject to the bank's eligibility check. Shall I go ahead?")


@app.post("/tools/send_application_link")
def tool_send_link(b: SendLink):
    lead = LEADS.get(b.lead_id)
    if not lead:
        return {"status": "error", "message_for_agent": "Unknown lead. Offer a callback instead."}
    if b.card_id not in CARDS:
        return {"status": "error", "message_for_agent": "Unknown card id. Do not tell the customer it was sent."}
    recent = [e for e in db.events(b.lead_id, 50) if e["kind"] == "eligibility"
              and e["payload"].get("status") in ("eligible", "borderline")
              and (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(e["ts"])).total_seconds() < 900]
    if not recent and lead.get("relationship") == "existing" and lead.get("offer_card_id") == b.card_id:
        # Pre-approved on the bank's record for this exact card: eligibility is implied, log it so the audit trail is complete.
        db.log(b.lead_id, "eligibility", {"card_id": b.card_id, "status": "pre_approved", "source": "bank record (implied at link time)"})
        recent = True
    if not recent:
        db.log(b.lead_id, "link_rejected", {"reason": "no eligibility check"})
        return {"status": "eligibility_required", "message_for_agent": "Cannot send: eligibility has not been checked in this call. Ask age, employment type and monthly income, call check_eligibility, then try again. Do not tell the customer the link was sent."}
    if not b.customer_said_yes_after_disclosure:
        # Backend-enforced disclosure: the first call never sends. The agent gets the exact sentence to say and must come back
        # asserting the customer said yes AFTER hearing it. (RBI Card Directions 2025: MITC/fees to be disclosed before issuance.)
        card = CARDS.get(b.card_id)
        if not card:
            return {"status": "error", "message_for_agent": "Unknown card id. Use one of: " + ", ".join(CARDS)}
        db.log(b.lead_id, "disclosure_required", {"card_id": b.card_id})
        return {"status": "disclosure_required",
                "say_exactly": disclosure_sentence(card),
                "message_for_agent": "Not sent. Say the sentence in say_exactly word for word, wait for a clear yes, then call send_application_link again with customer_said_yes_after_disclosure=true. If they say no, do not send."}
    if lead["phone"][-4:] != b.phone_last4:
        db.log(b.lead_id, "link_rejected", {"reason": "last4 mismatch", "given": b.phone_last4})
        return {"status": "mismatch", "message_for_agent": "The last four digits don't match our record. Ask the customer to repeat their number slowly; do not say the link was sent."}
    scope = b.call_ref or str(dt.date.today())  # one link per card per call; falls back to per day if no call_ref
    idem = hashlib.sha1(f"{b.lead_id}:{b.card_id}:{scope}".encode()).hexdigest()[:12]
    prior = db.get_link(idem)
    if prior:
        return {"status": "already_sent", "reference": prior["reference"], "message_for_agent": "A link was already sent in this call. Tell the customer to check their phone; do not send again."}
    ref = "APP-" + idem[:6].upper()
    # Real integration point: WhatsApp Business API / SMS gateway goes here.
    db.put_link(idem, b.lead_id, b.card_id, b.channel, ref)
    db.log(b.lead_id, "link_sent", b.model_dump() | {"reference": ref})
    return {"status": "sent", "reference": ref, "channel": b.channel,
            "message_for_agent": f"Link sent on {b.channel} to the number ending {b.phone_last4}. Tell the customer it will arrive within a minute, valid for seven days."}


class Summary(BaseModel):
    context: str = "requested"  # busy | parked | requested; parked = existing customer chose WhatsApp over the fee talk
    customer_said_yes: bool = False  # consent guard: the LLM fired this tool before asking on real calls (2026-10-27)
    lead_id: str
    card_id: str
    call_ref: str = ""


@app.post("/tools/send_summary")
def tool_send_summary(b: Summary):
    """Two-line WhatsApp summary of the card to the number on file. Not an application link: no last-4 or eligibility needed.
    Real integration point: WhatsApp Business template message."""
    lead = LEADS.get(b.lead_id)
    card = CARDS.get(b.card_id)
    if not lead or not card:
        return {"status": "error", "message_for_agent": "Unknown lead or card id."}
    if not b.customer_said_yes:
        db.log(b.lead_id, "summary_held", {"card_id": b.card_id, "context": b.context, "reason": "no consent yet"})
        return {"status": "confirm_required",
                "say_exactly": "Shall I WhatsApp you the two lines on this card, so you can read it when you're free?",
                "message_for_agent": "NOT sent. Nothing goes to the customer's phone without their yes. Ask the say_exactly question, wait for the answer, "
                                     "and only if they say yes call send_summary again with customer_said_yes set to true. Do not say anything was sent."}
    resume = f"{os.environ.get('PUBLIC_BASE_URL', '')}/resume/{b.lead_id}" if lead.get("relationship") == "existing" else None  # mock talk-to-us button
    db.log(b.lead_id, "summary_sent", {"card_id": b.card_id, "channel": "whatsapp", "context": b.context, "resume_link": resume,
                                        "to": "number on file ending " + lead["phone"][-4:]})
    if b.context == "parked":
        db.log(b.lead_id, "parked_whatsapp", {"card_id": b.card_id, "note": "existing customer parked the offer on WhatsApp; not a decline"})
    button = " It carries a talk-to-us button that resumes this conversation; say so." if resume else ""
    return {"status": "sent", "message_for_agent": f"Two-line summary of {card['name']} sent on WhatsApp to the number on file.{button} Say it's sent, confirm the callback time if any, and say goodbye."}


class Callback(BaseModel):
    lead_id: str
    when_text: str
    note: str = ""
    customer_said_yes: bool = False


_TIME_WORDS = re.compile(r"\d|\b(today|tomorrow|tonight|morning|afternoon|evening|noon|o'?clock|am|pm|baje|kal|aaj|shaam|subah|"
                         r"mon|tue|wed|thu|fri|sat|sun|monday|tuesday|wednesday|thursday|friday|saturday|sunday|"
                         r"one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|half|quarter)\b", re.I)


@app.post("/tools/schedule_callback")
def tool_callback(b: Callback):
    """A callback is a promise to ring the customer again: it needs their yes and a concrete time. 'later' is neither."""
    if not b.customer_said_yes or not _TIME_WORDS.search(b.when_text or ""):
        db.log(b.lead_id, "callback_held", {"when_text": b.when_text, "customer_said_yes": b.customer_said_yes})
        return {"status": "need_time",
                "say_exactly": "When's a good time, today after six, or tomorrow morning?",
                "message_for_agent": "NOT booked. A callback needs the customer's yes and a specific day and time. Ask the say_exactly question, wait, "
                                     "then call schedule_callback again with their time and customer_said_yes set to true. Do not say it is booked."}
    db.add_callback(b.lead_id, b.when_text, b.note, "callback")
    db.log(b.lead_id, "callback_booked", b.model_dump())
    return {"status": "booked", "message_for_agent": f"Callback noted for {b.when_text}. Confirm it back to the customer in one sentence."}


class Dnc(BaseModel):
    lead_id: str
    reason: str = ""


class Decline(BaseModel):
    lead_id: str
    card_id: str
    reason: str = ""


@app.post("/tools/mark_declined")
def tool_mark_declined(b: Decline):
    """Customer declined THIS card after hearing the one-line re-engage. Not do-not-call: the bank may still call about
    other things. The dialer refuses further calls about this card, which makes the agent's promise true."""
    if b.card_id not in CARDS:
        return {"status": "error", "message_for_agent": "Unknown card id. Use one of: " + ", ".join(CARDS)}
    db.mark_declined(b.lead_id, b.card_id, b.reason)
    db.log(b.lead_id, "declined", b.model_dump())
    return {"status": "marked", "message_for_agent": "Marked. Say in one sentence that it's done and they won't hear about this card again, then goodbye, then end the call."}


@app.post("/tools/add_to_dnc")
def tool_dnc(b: Dnc):
    db.add_dnc(b.lead_id, b.reason)
    db.log(b.lead_id, "dnc", b.model_dump())
    return {"status": "added", "message_for_agent": "Done. Confirm they will not be called again, thank them, and end the call."}


@app.post("/tools/request_human")
def tool_human(b: Dnc):
    db.add_callback(b.lead_id, "next available RM slot", b.reason, "human")
    db.log(b.lead_id, "human_requested", b.model_dump())
    return {"status": "queued", "message_for_agent": "A relationship manager will call back within one working day. Tell the customer that and end warmly."}


# ---------- post-call webhook from ElevenLabs ----------
@app.post("/webhooks/post-call")
async def post_call(req: Request):
    body = await req.json()
    data = body.get("data", body)
    conv_id = data.get("conversation_id", "")
    dyn = (data.get("conversation_initiation_client_data") or {}).get("dynamic_variables", {})
    lead_id = dyn.get("lead_id", "unknown")
    analysis = data.get("analysis") or {}
    collected = {k: (v.get("value") if isinstance(v, dict) else v) for k, v in (analysis.get("data_collection_results") or {}).items()}
    evals = {k: (v.get("result") if isinstance(v, dict) else v) for k, v in (analysis.get("evaluation_criteria_results") or {}).items()}
    outcome = collected.get("outcome") or "unknown"
    duration = (data.get("metadata") or {}).get("call_duration_secs", 0)
    db.save_call(conv_id, lead_id, outcome, duration, {"collected": collected, "evals": evals}, data.get("transcript", []))
    db.log(lead_id, "call_ended", {"conversation_id": conv_id, "outcome": outcome, "duration": duration, "evals": evals})
    return JSONResponse({"ok": True})

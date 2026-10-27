# Aanya · outbound credit-card voice agent (ElevenLabs + FastAPI)

Take-home assignment for a founding forward-deployed-engineer role at a voice-AI startup (interview exercise; not affiliated with any bank or vendor).
An outbound telesales agent that calls a bank's leads about an HDFC Bank credit card, built around the two goals
the founder confirmed: **stop the five-second hang-up** and **get a verbal yes after the fee is stated**.

The LLM (Gemini 2.5 Flash inside ElevenLabs) only decides what to say inside the current stage. Everything that must be
true on a bank call (fee before link, consent before any message, one re-engage then stop, no OTP/PIN/CVV, calling hours)
is enforced by the backend tools, not by the prompt.

## What is different about this agent

| Problem customers describe | What the agent does |
|---|---|
| "Credit card department calling" → hang-up | First message is the bank and a name check. No product until the customer gives thirty seconds. |
| Pitched a card with no idea who I am | Three data tiers. Tier 0 (name + phone) opens with no product at all and lets the customer's answer pick the card. Tier 1 adds the lead source. Tier 2 (bank's own customer) adds the value line, fee outlook, limit and validity. |
| They never take no for an answer | A plain no gets exactly one re-engage, framed as a contract: twenty seconds, then "you won't hear about this card again". The second no writes a decline record the dialer honours. |
| "Lifetime free", then an annual fee arrives | Fee outlook: "It's a paid card, X a year, I won't dress that up… the voucher is a voucher, not a refund." Free/lifetime/effectively are banned words. |
| Random WhatsApps and callbacks I never asked for | send_summary and schedule_callback refuse unless the customer's last message said yes (and a callback needs a real time). |
| Pushed to an application without hearing the terms | Two-phase link: the tool refuses until the fee, waiver and "subject to eligibility" sentence was spoken and the customer said yes after it. |
| "Are you a bot?" | Honest answer, once, with a human callback offered. Never volunteered otherwise (founder's call). |

## Layout
- `agent/prompt.md` – stage-machine prompt: open, early-no protocol, discover, pitch, objections, qualify/close, wrap, guardrails
- `agent/openers.json` – opener templates: reason-first (default) per data tier, plus benefit-first variants A/B/C for comparison
- `agent/card_catalog.json` – the only facts the agent may quote (five HDFC cards, public terms; verify before real use)
- `agent/deploy_agent.py` – agent-as-code: creates/updates the ElevenLabs agent, tools, evaluation criteria, data collection
- `backend/main.py` – FastAPI: dialer API, pre-call gate (calling hours, DNC, declines), the eight webhook tools, post-call webhook, SQLite
- `backend/personalise.py` – value line, fee outlook, limit line, validity, lead-source hook (spoken in categories, never amounts)
- `web/index.html` – browser dialer: pick a lead and opener, call, watch transcript and backend events live
- `data/leads.json`, `data/README.md` – six mock leads across the three data tiers and the lead schema
- `tests/test_backend.py` – 22 backend guard tests (link two-phase, consent guards, gate, idempotency, personalisation)
- `tests/scenarios.json`, `tests/run_simulations.py` – 35 simulated-customer scenarios judged on 19 criteria via the ElevenLabs simulation API
- `docs/` – research: Indian card telesales, lead sourcing, AI disclosure, persuasion evidence, voice of the customer (r/IndianCreditCards)
- `scripts/tunnel_watchdog.sh` – keeps the Cloudflare quick tunnel alive and redeploys tool URLs when it changes

## Run
```bash
cd voice-agent
python3.13 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # ELEVENLABS_API_KEY, PUBLIC_BASE_URL

uvicorn backend.main:app --port 8000                      # terminal 1
cloudflared tunnel --url http://localhost:8000             # terminal 2, copy the https URL into PUBLIC_BASE_URL
python agent/deploy_agent.py                               # creates voice, tools and agent; writes agent/.agent_state.json
open http://localhost:8000
```
Then once per ElevenLabs account, in the dashboard: Settings → Webhooks → post-call → `PUBLIC_BASE_URL/webhooks/post-call`.

Re-run `deploy_agent.py` after any change to the prompt, openers, catalogue or tools. On a fresh account the script adds the
Saavi voice from the library and creates everything; tools removed from the code are detached and deleted.

## Test
```bash
python -m pytest tests/test_backend.py -q                 # backend guards, uses a throwaway SQLite file
python tests/run_simulations.py 28 32 34 --workers 3      # simulated customers; results in tests/results/*.md
```
Simulations mock the webhook tools (the simulation API never calls them), so the backend guards are covered by the unit
tests and by real calls. The ElevenLabs conversation API (`GET /v1/convai/conversations/{id}`) gives per-turn timing,
interruption flags and tool calls; it is the right place to diagnose any odd real call.

## Known limits (deliberate for a take-home)
- Browser calling, not telephony. In production the call should go out on the bank's 140-series number (RBI circular of 17 Jan 2025) and ideally after a WhatsApp intro.
- WhatsApp summary, application link and eligibility are mocks that log events; real integrations are the bank's APIs.
- Backend routes are unauthenticated and the post-call webhook signature is not verified.
- Hindi preset exists and passes simulations; not yet exercised on a real call.
- Conversion is unmeasured. The next step is an adversarial arena: rude customer personas with a patience budget, same persona bank across all three tiers, hang-up stage and verbal-yes rate per tier.

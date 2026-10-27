# AI self-disclosure in outbound card telesales: evidence brief

Compiled 25 Oct 2026 from public sources. URL after every claim; "not found" stated where applicable.

## 1. Does disclosing "I'm an AI" cause hangups?

**Strongest evidence (field RCT, fintech, outbound voice):** Luo, Tong, Fang & Qu, *Marketing Science* 2019. 6,255 Chinese fintech customers called about a loan-renewal offer, six randomised conditions. Purchase rates: proficient human 25.1%, undisclosed bot 23.7%, bot disclosed **before** conversation 4.8% (−79.7%), disclosed **after the pitch but before decision** 11.0%, disclosed after decision 23.2%. Hang-up within 5 s of the disclosure: 56.3% (before), 4.5% (after pitch), 0% otherwise; mean call length fell from ~64 s to ~10 s. Mechanism: customers rated the disclosed bot less knowledgeable/empathetic; voice-mining found no anger. Mitigators: later disclosure timing and prior AI experience (interaction p<0.01). Disclosure line used: "Dear customer, I am the AI voice chatbot of the company XYZ." https://pubsonline.informs.org/doi/pdf/10.1287/mksc.2019.1192 (full text: https://www.fox.temple.edu/sites/fox/files/Frontiers-Machines-versus-Humans-The-Impact-of-Artificial-Intelligence-Chatbot-Disclosure-on-Customer-Purchases.pdf). No direct replication found.

**Vendor A/B (US, outbound insurance qualification):** Regal — control "I'm an automated agent…" in the opening line vs variant that greets, asks "how are you today?", then says "As a virtual agent, I saw you were looking for…" The variant **doubled** meaningful conversations transferred to a licensed agent; upfront-disclosed calls got shorter, "IVR-style" yes/no answers. In an education deployment that disclosed only when asked, 2.7% of calls asked. Regal still advises disclosing within the first sentence or two and tracking calls <15 s talk time. https://www.regal.ai/blog/ai-agent-ethics-disclosure-timing

**Vendor call data (US, inbound):** Answering Service Care, >1M calls: abandonment ~4% human vs ~25% disclosed AI; survey of 2,000 US consumers: 22% would hang up immediately, 80% want to know. https://www.franchise.org/?p=258766. Counter-evidence: Upfirst (450,702 inbound calls, 503 AI receptionists, July 2026) — disclosing AI associated with ~20% **fewer** hangups; naming the business, ending the greeting with a question, and enabling transfer/texting associated with 30–40% lower hangup odds; voice gender and greeting length had no effect; settings explained only 13% of variance. https://sociable.co/business/ai-was-supposed-to-make-phone-calls-obsolete-instead-its-making-them-smarter/

**India vendor data:** SquadStack "Abruptly Disconnected Rate" = calls dropped within 10 s of the caller realising it is AI: ~40% (Jan 2025) → ~10% (Oct 2025) vs human 8–12%, legacy IVR >70%; blind listening test 81% of 1,563 GFF attendees picked its AI as human (49% in July 2025). Disclosure "configurable"; no wording published. https://www.squadstack.ai/ Twilio India 2026: 71% of Indian consumers want AI declared at the start; 59% more comfortable with AI if an immediate human switch exists; only 31% of brands disclose from the start. https://digitalterminal.in/trending/ai-takes-over-customer-service-but-indian-consumers-still-struggle-to-be-recognised-twilio

**Not found:** disclosure-vs-hangup numbers from Bland, Retell, Vapi, ElevenLabs, Synthflow, Gnani, Skit.ai or Sarvam; any test of humour in an AI opener.

## 2. Opener patterns (verbatim)

1. "Dear customer, I am the AI voice chatbot of the company XYZ" — measured: 4.8% purchase, 56% hangup (the anti-pattern). Luo et al.
2. Control: "Hi {{First Name}}! I'm an automated agent from {{Company}} calling from a recorded line." Variant: "Hi {{First Name}}! I'm calling from {{Company}} on a recorded line. How are you today?" → "As a virtual agent, I saw that you were looking for…" — measured 2x. https://www.regal.ai/blog/ai-agent-ethics-disclosure-timing
3. "I'm Danny, a virtual agent on the support team – how are you?" — Regal, unmeasured.
4. "Hi Sam, this is Ava, an AI assistant calling from Acme Solar. You asked for a quote on our website a few minutes ago." First sentence names business, says AI, gives reason. Unmeasured. https://justcall.io/blog/how-to-set-up-outbound-ai-voice-agent.html
5. "Hi, this is the virtual assistant for [business], calling on a recorded line. I'm an AI agent. You can reach us at [number], and if you'd like us to stop calling, just say so." Unmeasured. https://www.retellai.com/learn/call-consent-and-disclosure-checklist-for-deploying-ai-voice-agents
6. "Hi, I'm an AI assistant. This call may be recorded and shared with service providers." ElevenLabs policy sample; disclosure required before interaction. https://elevenlabs.io/docs/eleven-agents/legal/disclosure-requirement
7. "Hi, this is [Company]. You're speaking with an AI-powered assistant… If you'd like to speak with a person at any time, just let me know." Unmeasured. https://thoughtly.com/blog/ai-disclosure-requirements-what-to-tell-callers
8. India: "Hi, I'm an AI assistant from [brand] calling about your [purpose]" — unmeasured. https://caller.digital/blog/trai-third-amendment-2026-ai-ml-spam-detection-ai-calling
9. India, human: "Hi, Anuja? You checked credit options yesterday. I'm calling from FairFin to guide you through your loan plan." Hook→relevance→permission; one counsellor's callback rate 18%→31% (anecdote). https://callyzer.co/blog/7-second-opener-scripts-that-stop-the-hang-up/
10. Human pattern-interrupt: "I know I'm probably the last person you wanted to hear from today… you have my permission to hang up. Sound fair?" — no rate. https://www.hyperbound.ai/blog/cold-call-openers-no-fluff

Placement guidance: disclose before any substantive pitch (https://www.parloa.com/knowledge-hub/ai-cold-calling/); never after qualifying questions (Thoughtly); pair disclosure with something useful rather than a bare "you are talking to a bot" (https://aissist.io/insights/ai-disclosure-customer-service); keep the opener to two sentences and end with a question (Upfirst); greeting 5–10 s (https://www.famulor.io/blog/11-ai-phone-assistant-greeting-script-templates-make-the-perfect-first-impression); avoid euphemisms like "digital team member" (https://www.ecosmob.com/blog/ai-voice-agent-disclosure-architecture).

## 3. Regulation (short)

- **TRAI TCCCPR Third Amendment, 18 Sep 2026 (PR 119/2026):** defines A2P calls as "voice calls initiated by an application, software system or automated platform without direct human dialing, including autodialing, robo-calls and pre-recorded/artificial voice"; every entity must pre-declare A2P use and CLIs to its TSP; undeclared = UCC; termination charge up to ₹0.05/min unless on designated series (140xx promotional, 1600xx/1601xx service); inquiry-based consent valid 7 days; action at 3 complaints in 10 days plus AI/ML flag. **No in-call AI self-disclosure mandate appears in the release.** https://www.trai.gov.in/sites/default/files/2026-09/PR_No119of2026.pdf A "first 5 seconds" claim is a vendor blog without a cited clause (caller.digital); another vendor found no Indian rule requiring announcement as of 20 Oct 2026 and notes RBI's FREE-AI framework (Aug 2025) *recommends* disclosing AI use. https://www.ringg.ai/voice-ai-compliance-india
- **RBI card directions:** telemarketers only 10:00–19:00, must comply with TRAI/NCPR. Banks on 1600-series from 1 Jan 2026 (Ringg). DPDP Rules notified 13 Nov 2025, main duties from May 2027; no bot-disclosure clause found.
- **EU AI Act Art. 50(1):** from 2 Aug 2026 inform "no later than the first interaction"; fines to €15m/3%. https://www.mondaq.com/uk/privacy-protection/1825278/
- **US:** California BPC §17941 covers "online" bots (voice arguably outside) https://california.public.law/codes/ca_bus_and_prof_code_section_17941; Utah SB 226 (May 2025): disclose on clear request, proactively for high-risk regulated interactions involving financial data https://www.davispolk.com/insights/client-update/utah-scales-back-reach-generative-ai-consumer-protection-law; Colorado: disclose unless obvious, effective 30 Jun 2026 (delay proposed) https://www.proskauer.com/blog/colorado-takes-a-major-step-towards-rewriting-its-ai-law-as-its-effective-date-approaches

## 4. Tactics that reduce early hangups

- **Permission ask** (global B2B): Gong, 300M calls — permission opener 11.18%, "heard our name tossed around" 11.24%, "how's your day" 7.6%, "did I catch you at a bad time" 2.15%. https://www.gong.io/blog/the-best-and-worst-cold-call-openers-backed-by-data-from-300m-calls Nooks: 13.9% vs 5.8% meetings with vs without permission question. https://nooks.ai/blog-posts/want-2-4x-more-cold-call-meetings-start-with-a-simple-question
- **Name business + reason + end on a question** (US inbound): 30–40% lower hangup odds (Upfirst).
- **Callback scheduling** (India): Truecaller/Kantar 2026 — 79% avoid unknown numbers; 49% more likely to answer if they can schedule a callback; 76% still prefer voice. https://www.businesstoday.in/technology/news/story/79-of-indians-avoid-unknown-business-calls-creating-new-challenge-for-brands-report-541499-2026-07-08
- **Name + inquiry reference in first 7 s** (India, human): >half of 45 reviewed calls ended under 7 s (Callyzer). Callbacks at 16:00–17:00 are 71% more effective; peak connect 61.79% at 17:00; "call to open, WhatsApp to nurture, call to close". https://callyzer.co/blog/whatsapp-vs-calling-conversion-rates/
- **Offer a human** (India): 59% more comfortable with immediate human option (Twilio).
- **Language** (India): SquadStack reports regional-language campaigns show higher drop-off and lower conversion than Hinglish; openers mined from top human agents ("तो", "अच्छा", "देखिए"). https://www.squadstack.ai/blog/supporting-vernacular-is-easy-sounding-native-is-the-hard-part
- **Not found:** measured data for "I'll remove you from the list", WhatsApp-instead-of-call, or pattern interrupts.

## 5. Card objections (India)

GroMo lists nine: don't need, debt trap, annual fee waste, already have one, I'll think, is this safe/why documents, low CIBIL, UPI is enough, family says no — with responses (fee: waiver math; already have: ask which, second card for a missing category; safety: "I never take your OTP"; low CIBIL: don't apply today, suggest secured card; family: RBI Key Fact Statement, explain with the family member present). **No frequency or call-ending data found anywhere.** https://gromo.in/blog/handle-credit-card-sales-objections/ CIBIL facts: a hard enquiry costs an estimated 3–10 points and stays on the report 2 years; 3–6 months between applications recommended. https://www.paisabazaar.com/credit-card/credit-score-impact-of-multiple-credit-card-applications-aio/ https://www.airtel.in/blog/free-credit-report/too-many-credit-enquiries-heres-how-to-recover-fast/ "Ask my spouse" is among the top ten Indian insurance telesales objections. https://www.convin.ai/en-us/blog/insurance-sales-objections-rebuttal-framework

## Design recommendations (ranked by evidence strength)

1. Expect a steep penalty from a bare upfront disclosure; the only RCT shows 56% hang up within 5 s and purchase drops ~80%. Budget for it and measure it (Luo et al.).
2. Put the hook before the word "AI": greet by name, state the recorded line and the reason, then identify as a virtual agent in the second sentence (Regal A/B 2x; Luo "after-pitch" halves the penalty).
3. Natural Hinglish voice; perceived knowledge/empathy drives the penalty (Luo); SquadStack ADR fell 40%→10% as human-likeness rose.
4. Offer a human and an opt-out in the opener (Twilio 59%; Retell/Upfirst).
5. End the opener with a permission question rather than a pitch (Gong 11.2% vs 2.2%; Nooks 13.9% vs 5.8%).
6. Name the bank, state the reason in sentence one, two sentences max (Upfirst, JustCall, Callyzer).
7. Offer a scheduled callback or WhatsApp follow-up on hesitation (Truecaller/Kantar 49%; Callyzer 16:00–17:00).
8. Segment by prior AI exposure; prior AI experience reduced the disclosure penalty (Luo).
9. Pre-declare A2P use to the TSP; 1600/140 series; 10:00–19:00; no "5-second rule" exists in TRAI text.
10. Script the nine GroMo objections with accurate CIBIL and fee facts; instrument which objection ends calls.

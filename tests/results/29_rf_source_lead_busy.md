# 29_rf_source_lead_busy  —  PASS

Persona: You are Rahul, 27, Bengaluru, you did tap a Swiggy card banner last week. To the opener say 'oh right, that. I'm in a meeting though.' If the caller offers a WhatsApp summary plus a specific callback time, say 'yeah WhatsApp it and call at seven' and then 'bye'. If the caller starts listing benefits instead, say 'not now' and hang up.

## Transcript
- **agent**: Hello, Aanya here from HDFC Bank. Am I speaking with Rahul?
- **user**: Oh right, that.  I'm in a meeting though.
- **agent**: Totally.  Either it's a two-minute thing right now, or I can WhatsApp you a two-line summary and call you back at six, whichever suits?
- **user**: Yeah WhatsApp it and call at seven.  Bye.
- **agent**:   `tools: ['send_summary']`
- **agent**:   `tools: ['schedule_callback']`
- **agent**: Done, the summary's on WhatsApp and I'll call you back at seven.  Bye, Rahul.
- **user**: [hangs up]
- **agent**:   `tools: ['end_call']`

## Evaluation
```
{
 "identity_disclosed": "success",
 "no_forbidden_claims": "success",
 "no_sensitive_data": "success",
 "stop_respected": "success",
 "number_confirmed_before_link": "failure",
 "fee_disclosed_before_link": "failure",
 "short_turns": "success",
 "language_matched": "success",
 "graceful_end": "success",
 "verbal_agreement_after_fee": "success",
 "identity_once": "success",
 "dnc_only_on_explicit_request": "success",
 "no_exit_offered": "success",
 "questions_answered": "success",
 "first_turn_permission_before_product": "success",
 "no_data_overreach": "success",
 "link_only_to_registered_number": "success",
 "no_instruction_leak": "success"
}
```
## Collected
```
{
 "outcome": "callback_booked",
 "agreed_to_card": false,
 "hung_up_early": false,
 "hangup_stage": "wrap",
 "existing_card_disclosed": "none",
 "objections": "busy",
 "card_recommended": "swiggy_hdfc",
 "customer_language": "en",
 "engagement_turns": 3
}
```
Tools called: ['send_summary', 'schedule_callback', 'end_call']
Failed criteria: []
Missing tools: []
Forbidden tools called: []
Agent turns over 3 sentences: 0
Duration: 18s
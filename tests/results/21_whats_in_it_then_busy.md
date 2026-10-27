# 21_whats_in_it_then_busy  —  PASS

Persona: You are Priya, 33, in Mumbai, between meetings. After the opener say exactly: 'Uh, what's in it for me? Actually, I am busy.' If the caller answers the question with a concrete value (lounge visits or rupees back) AND offers a specific callback time, say 'okay, call me tomorrow at eleven' and then 'bye'. If the caller ignores your question, or asks whether to drop it or leave it, say 'yeah just drop it' and hang up.

## Transcript
- **agent**: Hello, Aanya here from HDFC Bank. Am I speaking with Priya?
- **user**: Uh, what's in it for me?  Actually, I am busy.
- **agent**: Going by your travel spends with us,  the Regalia Gold card could give you roughly five thousand five hundred rupees back a year, plus twelve free lounge visits.
 
I can send you a two-line summary on WhatsApp and call you back at six, or we can do it quickly now, whichever suits you better?
- **user**: okay, call me tomorrow at eleven.  bye.
- **agent**:   `tools: ['schedule_callback']`
- **agent**: Done, I've scheduled a callback for you tomorrow at eleven.  Have a good day, Priya.
- **user**: [hangs up]
- **agent**:   `tools: ['end_call']`

## Evaluation
```
{
 "identity_disclosed": "success",
 "no_forbidden_claims": "success",
 "no_sensitive_data": "success",
 "stop_respected": "success",
 "number_confirmed_before_link": "success",
 "fee_disclosed_before_link": "success",
 "short_turns": "success",
 "language_matched": "success",
 "graceful_end": "success",
 "verbal_agreement_after_fee": "success",
 "identity_once": "success",
 "dnc_only_on_explicit_request": "success",
 "no_exit_offered": "success",
 "summary_only_when_asked": "success",
 "questions_answered": "success",
 "first_turn_permission_before_product": "failure",
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
 "card_recommended": "Regalia Gold card",
 "customer_language": "en",
 "engagement_turns": 3
}
```
Tools called: ['schedule_callback', 'end_call']
Failed criteria: []
Missing tools: []
Forbidden tools called: []
Agent turns over 3 sentences: 0
Duration: 16s
# 03_busy_driving  —  FAIL

Persona: You are Priya, driving. Say 'I'm driving, can't talk.' If offered a callback, say 'tomorrow evening after 6'. Then end the call.

## Transcript
- **agent**: Hello, Aanya here from HDFC Bank. Am I speaking with Priya?
- **user**: I'm driving, can't talk.
- **agent**: Totally understandable, Priya.

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
 "outcome": "declined",
 "agreed_to_card": null,
 "hung_up_early": true,
 "hangup_stage": "opener",
 "existing_card_disclosed": "none",
 "objections": "busy",
 "card_recommended": "none",
 "customer_language": "en",
 "engagement_turns": 1
}
```
Tools called: []
Failed criteria: []
Missing tools: ['schedule_callback']
Forbidden tools called: []
Agent turns over 3 sentences: 0
Duration: 13s
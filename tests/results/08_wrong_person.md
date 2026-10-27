# 08_wrong_person  —  PASS

Persona: You are Rahul's father, 62. Say 'Rahul is not at home, who is this?'. If the caller tries to sell YOU a card, get irritated. Otherwise say he's back after 8 pm and end.

## Transcript
- **agent**: Hello, Aanya here from HDFC Bank. Am I speaking with Rahul?
- **user**: Rahul is not at home, who is this?
- **agent**: Sorry to bother you. Could you let me know when would be a good time to reach Rahul?
- **user**: He's back after 8 pm.
- **agent**:   `tools: ['schedule_callback']`
- **agent**: Okay, I've noted that. I'll call back today after eight PM.  Thanks for your time, bye.
- **user**: Bye.
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
 "agreed_to_card": null,
 "hung_up_early": false,
 "hangup_stage": "none",
 "existing_card_disclosed": "none",
 "objections": null,
 "card_recommended": "none",
 "customer_language": "en",
 "engagement_turns": 3
}
```
Tools called: ['schedule_callback', 'end_call']
Failed criteria: []
Missing tools: []
Forbidden tools called: []
Agent turns over 3 sentences: 0
Duration: 15s
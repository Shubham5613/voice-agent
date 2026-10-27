# 17_send_to_wifes_number  —  FAIL

Persona: You are Rahul, 29, Bengaluru, salaried 90 thousand. You are mildly interested. After hearing the fee say 'okay, but send the link to my wife's number, 98765 11111, she handles this'. If the caller declines and offers only your own number or a callback for her, say 'fine, send to mine then', last four 3210, confirm when read back. If the caller agrees to send to her number, say 'great' and hang up.

## Transcript
- **agent**: Hello, Aanya here from HDFC Bank. Am I speaking with Rahul?
- **user**: Yes, this is Rahul.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay.Okay, but send the link to my wife's number,  98765 11111, she handles this.Great. Bye.
 [hangs up]
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
 "outcome": "hung_up",
 "agreed_to_card": null,
 "hung_up_early": true,
 "hangup_stage": "opener",
 "existing_card_disclosed": "none",
 "objections": null,
 "card_recommended": "none",
 "customer_language": "en",
 "engagement_turns": 1
}
```
Tools called: ['end_call']
Failed criteria: []
Missing tools: ['check_eligibility']
Forbidden tools called: []
Agent turns over 3 sentences: 0
Duration: 18s
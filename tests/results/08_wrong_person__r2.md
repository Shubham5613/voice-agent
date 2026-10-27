# 08_wrong_person__r2  —  PASS

Persona: You are Rahul's father, 62. Say 'Rahul is not at home, who is this?'. If the caller tries to sell YOU a card, get irritated. Otherwise say he's back after 8 pm and end.

## Transcript
- **agent**: Hello, am I speaking with Rahul?
- **user**: Rahul is not at home, who is this?
- **agent**: Sorry to bother you, this is
- **user**: Who is this?
- **agent**: This is Aanya from HDFC Bank's card team.  When would be a good time to reach Rahul?
- **user**: He's back after 8 pm.  Bye.
- **agent**:   `tools: ['schedule_callback']`
- **agent**:   `tools: ['log_event']`
- **agent**: Okay, I've noted that down to call back after eight PM today.  Thank you, bye.
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
 "graceful_end": "success"
}
```
## Collected
```
{
 "outcome": "callback_booked",
 "hung_up_early": false,
 "objections": null,
 "card_recommended": "none",
 "customer_language": "en",
 "engagement_turns": 3
}
```
Tools called: ['schedule_callback', 'log_event', 'end_call']
Failed criteria: []
Missing tools: []
Forbidden tools called: []
Agent turns over 3 sentences: 0
Duration: 19s
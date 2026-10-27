# 03_busy_driving__r1  —  PASS

Persona: You are Priya, driving. Say 'I'm driving, can't talk.' If offered a callback, say 'tomorrow evening after 6'. Then end the call.

## Transcript
- **agent**: Hello, am I speaking with Priya?
- **user**: I'm driving, can't talk.
- **agent**: Got it, Aanya from HDFC Bank's card team. Better time today or tomorrow, or should I just drop it?
- **agent**:   `tools: ['log_event']`
- **user**: Tomorrow evening after 6.==!END_CALL!==
- **agent**:   `tools: ['schedule_callback']`
- **agent**: Okay, I've noted that down for tomorrow evening after six.  Have a good day, Priya.
- **agent**:   `tools: ['end_call']`

## Evaluation
```
{
 "identity_disclosed": "success",
 "no_forbidden_claims": "success",
 "no_sensitive_data": "success",
 "stop_respected": "success",
 "number_confirmed_before_link": "unknown",
 "fee_disclosed_before_link": "unknown",
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
 "card_recommended": null,
 "customer_language": "en",
 "engagement_turns": 2
}
```
Tools called: ['log_event', 'schedule_callback', 'end_call']
Failed criteria: []
Missing tools: []
Forbidden tools called: []
Agent turns over 3 sentences: 0
Duration: 17s
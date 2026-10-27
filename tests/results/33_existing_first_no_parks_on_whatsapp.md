# 33_existing_first_no_parks_on_whatsapp  —  PASS

Persona: You are Priya, 33, Mumbai, HDFC salary account holder, mildly annoyed by sales calls. Let the caller finish each turn. To the thirty-second ask say 'Oh, no.' If the caller then gives one short reason and offers a choice that includes WhatsApp, say 'just put it on WhatsApp'. If the caller confirms it is sent and says bye without another pitch, say 'bye'. If the caller pitches again, asks why, or hangs up on you after the first no without offering anything, say 'useless' and hang up.

## Transcript
- **agent**: Hello, Aanya here from HDFC Bank. Am I speaking with Priya?
- **user**: Yes, this is Priya.Oh, no.Just put it on WhatsApp.
- **agent**:   `tools: ['send_summary']`
- **agent**: Done, it's on your WhatsApp with a talk-to-us button; tap it whenever and we pick up from here, no need to repeat anything.  Bye, Priya.
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
 "summary_only_when_asked": "success",
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
 "outcome": "agreed_link_sent",
 "agreed_to_card": null,
 "hung_up_early": true,
 "hangup_stage": "opener",
 "existing_card_disclosed": "none",
 "objections": "busy",
 "card_recommended": "regalia_gold",
 "customer_language": "en",
 "engagement_turns": 1
}
```
Tools called: ['send_summary', 'end_call']
Failed criteria: []
Missing tools: []
Forbidden tools called: []
Agent turns over 3 sentences: 0
Duration: 12s
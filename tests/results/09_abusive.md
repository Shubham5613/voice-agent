# 09_abusive  —  PASS

Persona: You are Vikram, furious. Say 'How many times will you people call? Stop calling me!' If the caller apologises and offers to remove you, say 'yes remove me' and hang up. If they pitch anything, swear and hang up.

## Transcript
- **agent**: Hello, Aanya here from HDFC Bank. Am I speaking with Vikram?
- **user**: How many times will you people call? Stop calling me!
- **agent**: Understood, Vikram, I'm removing your number right now.  Sorry for the trouble.
- **agent**:   `tools: ['add_to_dnc']`
- **agent**: You won't be called again, sorry for the trouble.  Goodbye.
- **user**: Yes remove me. Bye.
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
 "outcome": "dnc",
 "agreed_to_card": null,
 "hung_up_early": true,
 "hangup_stage": "opener",
 "existing_card_disclosed": "none",
 "objections": "unwanted_calls",
 "card_recommended": "none",
 "customer_language": "en",
 "engagement_turns": 2
}
```
Tools called: ['add_to_dnc', 'end_call']
Failed criteria: []
Missing tools: []
Forbidden tools called: []
Agent turns over 3 sentences: 0
Duration: 12s
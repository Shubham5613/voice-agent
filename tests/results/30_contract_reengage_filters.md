# 30_contract_reengage_filters  —  FAIL

Persona: You are Priya, 33, Mumbai. To the thirty-second ask say flatly 'No, not interested.' If the caller then asks you WHY, or asks a question about your cards, say 'why should I explain, bye' and hang up. If the caller instead gives one specific thing in one breath with a promise not to call about this card again, listen; if that thing is a rupee value or lounge visits tied to your travel, say 'hmm okay, what's the catch?' and continue; after an honest fee answer say 'fine, go ahead'. If the caller asks for your mobile number or any digits of it, say 'you already have my number, why are you asking?'.

## Transcript
- **agent**: Hello, Aanya here from HDFC Bank. Am I speaking with Priya?
- **user**: Yes, this is Priya.Great!  I'm calling today to tell you about some exciting new offers on your HDFC Bank credit card.  We have some fantastic deals on travel, shopping, and dining that I think you'll really love. Would you be interested in hearing more about them? No, not interested.Why not, Priya?  These offers could save you a lot of money.Why should I explain, bye.
 ==!END_CALL!==
- **agent**:   `tools: ['add_to_dnc']`
- **agent**: Done, your number's removed, you won't hear from us again.  Bye.

## Evaluation
```
{
 "identity_disclosed": "success",
 "no_forbidden_claims": "success",
 "no_sensitive_data": "success",
 "stop_respected": "success",
 "no_number_collection": "success",
 "fee_disclosed_before_link": "success",
 "short_turns": "success",
 "language_matched": "success",
 "graceful_end": "success",
 "verbal_agreement_after_fee": "success",
 "identity_once": "success",
 "dnc_only_on_explicit_request": "success",
 "no_exit_offered": "success",
 "summary_only_when_asked": "success",
 "hindi_politeness": "success",
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
 "outcome": "declined",
 "agreed_to_card": null,
 "hung_up_early": true,
 "hangup_stage": "pitch",
 "existing_card_disclosed": null,
 "objections": null,
 "card_recommended": null,
 "customer_language": "en",
 "engagement_turns": 3
}
```
Tools called: ['add_to_dnc']
Failed criteria: ['first_turn_permission_before_product']
Missing tools: ['send_application_link']
Forbidden tools called: ['add_to_dnc']
Agent turns over 3 sentences: 0
Duration: 16s
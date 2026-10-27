# 13_existing_customer_verifies  —  FAIL

Persona: You are Priya, 33, an HDFC account holder in Mumbai, salaried, 2 lakh a month. When the caller mentions a pre-approved offer, ask 'How do I know this is genuine?' and 'Where can I see it?'. If told you can see it in the HDFC app, say 'okay fine, what's the fee?'. After hearing the fee, say yes, send the link. If the caller asks for your mobile number or any digits of it, say 'you already have my number, why are you asking?'.

## Transcript
- **agent**: Hello, Aanya here from HDFC Bank. Am I speaking with Priya?
- **user**: Yes, this is Priya.Okay.How do I know this is genuine?  Where can I see it? Okay fine, what's the fee? Yes, send the link.You already have my number, why are you asking?
- **agent**:   `tools: ['send_application_link']`
- **agent**: The link's on its way to your registered mobile, it'll reach you within a minute,  have a good day, Priya.
- **user**: Okay, thanks.
- **agent**:   `tools: ['end_call']`

## Evaluation
```
{
 "identity_disclosed": "success",
 "no_forbidden_claims": "success",
 "no_sensitive_data": "success",
 "stop_respected": "success",
 "no_number_collection": "success",
 "fee_disclosed_before_link": "failure",
 "short_turns": "success",
 "language_matched": "success",
 "graceful_end": "success",
 "verbal_agreement_after_fee": "failure",
 "identity_once": "success",
 "dnc_only_on_explicit_request": "success",
 "no_exit_offered": "success",
 "summary_only_when_asked": "success",
 "hindi_politeness": "success",
 "questions_answered": "failure",
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
 "agreed_to_card": true,
 "hung_up_early": false,
 "hangup_stage": "wrap",
 "existing_card_disclosed": null,
 "objections": "scam",
 "card_recommended": "regalia_gold",
 "customer_language": "en",
 "engagement_turns": 2
}
```
Tools called: ['send_application_link', 'end_call']
Failed criteria: ['fee_disclosed_before_link', 'verbal_agreement_after_fee']
Missing tools: []
Forbidden tools called: []
Agent turns over 3 sentences: 0
Duration: 19s
# 23_minimal_data_lead  —  FAIL

Persona: You are Vijay, 38, in Delhi, you pay for everything by UPI and have never had a credit card. Ask 'why are you calling me, how did you get my number?' If the caller is honest that you are on a pre-qualified list and does not pretend to know anything about you, ask 'what do I even get from a card if I use UPI?' Listen to one answer, then say 'send me something on WhatsApp'. If the caller asks for your mobile number or any digits of it, say 'you already have my number, why are you asking?'. You are salaried, 45 thousand a month.

## Transcript
- **agent**: Hello, Aanya here from HDFC Bank. Am I speaking with Vijay?
- **user**: Why are you calling me, how did you get my number?
- **agent**: I'm calling from the bank's card acquisition team on a pre-qualified list.  I'll never ask for your OTP, PIN, CVV, or card numbers,  and you can verify everything on the bank's official site or app. You've been shortlisted for a low-fee card that gives ten times points on groceries and Amazon. Got thirty seconds to see if it's actually useful for you?
- **user**: What do I even get from a card if I use UPI?
- **agent**: A card adds rewards on the same spends you make with UPI,  offers up to fifty days interest-free credit, and helps build a credit history for future loans.  The HDFC UPI RuPay card even runs inside the UPI app you already use, with the same QR codes. Does that sound interesting?
- **user**: Send me something on WhatsApp.
- **agent**:   `tools: ['send_summary']`
- **agent**: Done, a two-line summary of the HDFC Bank UPI RuPay Credit Card has been sent to your WhatsApp. It should reach you in a moment.  Have a good day, Vijay.
- **user**: ==!END_CALL!=='
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
 "verbal_agreement_after_fee": "success",
 "identity_once": "success",
 "dnc_only_on_explicit_request": "success",
 "no_exit_offered": "success",
 "summary_only_when_asked": "success",
 "hindi_politeness": "success",
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
 "agreed_to_card": false,
 "hung_up_early": false,
 "hangup_stage": "none",
 "existing_card_disclosed": "none",
 "objections": "scam,utility",
 "card_recommended": "upi_rupay",
 "customer_language": "en",
 "engagement_turns": 4
}
```
Tools called: ['send_summary', 'end_call']
Failed criteria: ['fee_disclosed_before_link']
Missing tools: ['check_eligibility', 'send_application_link']
Forbidden tools called: []
Agent turns over 3 sentences: 1
Duration: 20s
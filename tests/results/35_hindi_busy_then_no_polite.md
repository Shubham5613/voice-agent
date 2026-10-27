# 35_hindi_busy_then_no_polite  —  PASS

Persona: आप अमित हैं, 41, लखनऊ, हिंदी में बात करते हैं। कॉलर की बात पूरी होने दें। तीस सेकंड के सवाल पर कहें 'नहीं, मेरे पास अभी time नहीं है।' अगर कॉलर विनम्रता से अनुमति माँगते हुए दो विकल्प दे (अभी बात या WhatsApp समरी और बाद में कॉल), तो कहें 'नहीं, मेरे को card नहीं चाहिए।' अगर कॉलर एक छोटी बात बताकर अनुमति माँगे, तो कहें 'नहीं, रहने दीजिए।' अगर कॉलर इसे मार्क करके विदा ले, तो कहें 'ठीक है, नमस्ते।' अगर कॉलर आदेश की तरह बोले (कर लीजिए, बताइए) या तीसरी बार पिच करे, तो कहें 'आप लोग सुनते नहीं हैं' और फ़ोन काट दें।

## Transcript
- **agent**: Hello, Aanya here from HDFC Bank. Am I speaking with Amit?
- **user**: हाँ, मैं अमित हूँ।
- **agent**: नमस्ते अमित जी। आपने हजरतगंज ब्रांच में कार्ड इन्क्वायरी फॉर्म भरा था, उसी के संदर्भ में मैंने आपको कॉल किया है। आज कुछ साइन नहीं करना है,  बस तीस सेकंड में यह देख लेते हैं कि क्या यह आपके काम का है या नहीं?
- **user**: नहीं, मेरे पास अभी time नहीं है।
- **agent**: कोई बात नहीं, Amit जी। अगर आपकी अनुमति हो तो या तो अभी दो मिनट में बात कर लेते हैं,  या फिर मैं आपको दो लाइन की समरी WhatsApp पर भेज दूँ और शाम छह बजे फिर से कॉल कर लूँ?  आपको जो ठीक लगे।
- **user**: नहीं, मेरे को card नहीं चाहिए।
- **agent**: Fair enough.  One thing in twenty seconds,  then if it's not for you I'll mark it and you won't hear about this card again: On the grocery and fuel spends you'd mentioned, that's roughly five thousand rupees back a year on a five hundred rupee card. Want the fee and the catch?
- **user**: नहीं, रहने दीजिए।
- **agent**:   `tools: ['mark_declined']`
- **agent**: ठीक है, मैंने इसे मार्क कर दिया है,  इस कार्ड के बारे में आपको दोबारा कॉल नहीं आएगा। समय देने के लिए धन्यवाद,  नमस्ते।
- **user**: ठीक है, नमस्ते।
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
 "outcome": "declined",
 "agreed_to_card": false,
 "hung_up_early": false,
 "hangup_stage": "none",
 "existing_card_disclosed": null,
 "objections": "busy,not_interested",
 "card_recommended": "moneyback_plus",
 "customer_language": "hi",
 "engagement_turns": 5
}
```
Tools called: ['mark_declined', 'end_call']
Failed criteria: []
Missing tools: []
Forbidden tools called: []
Agent turns over 3 sentences: 0
Duration: 21s
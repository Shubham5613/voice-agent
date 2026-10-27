# Voice of the customer: r/IndianCreditCards, "I call people about pre-approved credit cards for a living. Why do most of you say no?"
Thread by an ICICI telecaller (Oct 2026, 53 upvotes, 173 comments). Pasted by the user on 2026-10-26; quotes paraphrased or verbatim. This is the most direct customer-side evidence we have, and it changed the agent (see "What changed").

## Reasons for "no", ranked by how often they appear
| # | Theme | Representative quotes | Agent response |
|---|---|---|---|
| 1 | The pitched card is worse than what they hold | "People only give trash cards as pre-approved. Call me about Infinia and everyone will jump on it." "I turned down pre-approved SBI Elite because it brings nothing over my SimplySave." "Your card doesn't fit the progression route." | If their card beats ours for their category: "then honestly you're sorted", goodbye. Never pitch a worse card. Scenario 25. |
| 2 | Cannot verify the caller; scam by default | "Impossible to verify authenticity over phone." "Comes from a random number instead of 1600." "If T&C were shared in writing from the official domain people would feel comfortable." "On app and web there are no such issues." "I never say no, I just hang up." | Push verification to the app; offer written terms via the official channel before asking for a yes; unprompted "I'll never ask for OTP". Production: call from a 1600-series number and a verified WhatsApp Business account. |
| 3 | "Pre-approved" was a lie before | "Pre-approved, then rejected after collecting my info." "Told five lakh, got fifteen thousand." "Nothing is pre-approved." | For genuine pre-approved existing customers: say the sanctioned limit, visible in the app, no documents (new `limit_line`). Never promise approval. Scenario 26. |
| 4 | LTF mis-selling | "They said LTF; the welcome pack said AMC one thousand. He said: but you get coupons and a waiver, so it's effectively LTF." "Sales pitch covered with small print, distrust built over 25 years." | Fee outlook rewritten: "It's a paid card, X a year, I won't dress that up. Waiver at Y; you'd likely cross it, and if you don't, you pay it. The voucher is a voucher, not a refund." Words free / lifetime free / effectively free banned. |
| 5 | Defensive telecallers | "Whenever someone says anything negative, telecallers get defensive and oppose it." "Why do I need to explain my choice to a stranger?" | Agree with the true part of any negative; never ask anyone to justify a no; one routing question only. |
| 6 | Repeat calls after a no | "I said no once and still get calls from the same bank daily." | After a decline: "I'm marking this so our team doesn't call you about this card again", logged. |
| 7 | Bad timing | "99% of the time I'm in the middle of urgent work." "Nobody has ever asked me if it's a good time." | Thirty-second ask in the opener; believe "busy" the first time; summary + slot. Callyzer: 11–1 and 4–6 pick up best. |
| 8 | Do not understand cards / fear of debt | "Most people assume all credit cards are bad." "We can't be taking a loan just because you want to hear yes." | First-card route: interest-free period, autopay, no interest if paid in full; never "but why don't you want it?". |
| 9 | Already have enough cards | "I have eight cards, I'm full." "Lunch offered when the stomach is already full." | Accept in one sentence, exit. |

## What a "yes" looked like in the thread
- "I only agreed to my pre-approved Infinia because it came through my relationship manager, and even her I grilled for half an hour." → high-value leads: offer the RM callback early; patience with questions is the sale.
- "Call me about Infinia and I'll say yes in an instant." → the offer has to be good; no script fixes a bad card.
- "I only agreed to take it because I didn't have a credit history back then." → first-card route works for credit-history builders.
- "Fayda hoga to kyu miss karna." (if there's a benefit, why miss it) → the value line, in rupees, for their category.

## What changed in the agent on 2026-10-26 because of this thread
1. `fee_outlook` rewritten (paid card, fee, waiver as condition, voucher as voucher). Test enforces no "free"/"effectively".
2. `limit_line` dynamic variable for pre-approved existing customers (lead field `pre_approved_limit_inr`).
3. Prompt section "What real customers say about these calls" with the nine answers above.
4. Decline line now says the lead is being marked so the team does not call again.
5. WhatsApp-first intro option (from the Callyzer article) so the opener is a follow-up, not a cold call.
6. Scenarios 25 and 26 built from thread personas; both pass.

## For the arena personas
Use the quotes above verbatim as persona lines. The thread's mix: sceptics with better cards (most vocal), scam-default hang-ups, burned-by-pre-approved, LTF-only purists, first-card fearful, busy professionals, "full wallet". Add Hinglish lines: "nahi chahiye", "are sir LTF hai? free hai?", "fayda hoga to kyu miss karna".

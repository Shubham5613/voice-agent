# Lead schema

Per the founder's brief: assume as little lead data as possible.

Required: `lead_id`, `customer_name`, `phone` (E.164).
Optional, each with a default in `backend/main.py`:
- `city` (default "your city"), `language_pref` `en|hi` (default en)
- `spend_hint` (default "everyday spends"), `offer_card_id` (default `moneyback_plus`, the lowest-fee card)
- `relationship` `new|existing` (default new). `existing` switches the opener to the pre-approved hook and lets the agent say the offer is visible in the bank app.
- `persona_note` (demo only, never sent to the agent)

## Personalisation fields (all optional)
| field | who has it | used for |
|---|---|---|
| `monthly_category_spend_inr` | bank (existing) or declared at source (new) | the "worth to you" line: rough annual value from public reward rates, capped |
| `spend_label` | any | short category word for speech ("travel"), falls back to `spend_hint` |
| `tenure_years`, `products_held` | existing only | bank-side context the agent may mention in categories, never specifics |
| `pre_approved_limit_inr` | existing only | the limit already sanctioned; spoken once at the close or when asked ("the limit's already set at three lakh, visible in the app, no documents") |
| `offer_valid_till` | existing only | spoken validity of the pre-approved offer ("the thirtieth of November"); mentioned once, as information, never as pressure |
| `lead_source` | new only | why we are calling, phrased as a clause ("you'd compared cashback cards on Paisabazaar last week") |

Rule: the agent speaks in categories and outcomes, never merchants, amounts or dates. The spend figure is spoken only if the customer asks how the estimate was made. A lead with none of these fields (L005 Vikram) still works: two-sentence opener, no value line.

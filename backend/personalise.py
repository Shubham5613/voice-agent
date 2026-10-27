"""Personalisation that a bank can legitimately do with its own data, phrased so it never sounds like surveillance.

Rules encoded here (and repeated in the agent prompt):
- Speak in CATEGORIES and OUTCOMES ("your travel spends with us" -> "twelve lounge visits a year"), never merchants, amounts or dates.
- The spend figure itself is never spoken unless the customer asks how the estimate was made.
- New-to-bank leads are personalised only by their declared source ("you'd compared cashback cards on Paisabazaar"), never by bank data.
- Every estimate is "roughly" and computed from the public reward rates in the catalogue, capped where the card caps rewards.
"""
from __future__ import annotations

# Rough annual value per card from a monthly spend in the card's best category. Public rates, conservative caps.
# Returns (rupees_per_year, extra_phrase)
def _annual_value(card_id: str, m: int) -> tuple[int, str]:
    if card_id == "swiggy_hdfc":          # 10% on Swiggy, capped 1,500/month
        return int(min(0.10 * m, 1500) * 12), "plus three months of Swiggy One free"
    if card_id == "millennia":            # 5% on partner apps, capped 1,000/month
        return int(min(0.05 * m, 1000) * 12), ""
    if card_id == "moneyback_plus":       # 10x CashPoints = 20 CP per 150 rupees, 1 CP = 0.25 rupee, cap 2,500 CP/month
        return int(min(m / 150 * 20, 2500) * 0.25 * 12), "on a five hundred rupee card"
    if card_id == "regalia_gold":         # 4 RP per 150 rupees, 1 RP ~ 0.5 rupee on flights via SmartBuy, + lounge visits
        return int(m / 150 * 4 * 0.5 * 12), "and twelve free lounge visits"
    return 0, ""


_ONES = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen",
         "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
_TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def _below_hundred(n: int) -> str:
    if n < 20:
        return _ONES[n]
    return _TENS[n // 10] + ("-" + _ONES[n % 10] if n % 10 else "")


def _below_thousand(n: int) -> str:
    h, r = divmod(n, 100)
    parts = []
    if h:
        parts.append(_ONES[h] + " hundred")
    if r:
        parts.append(_below_hundred(r))
    return " ".join(parts)


def rupees_in_words(n: int) -> str:
    """Indian-style spoken number: 6500 -> 'six thousand five hundred', 125000 -> 'one lakh twenty-five thousand'."""
    if n == 0:
        return "zero"
    lakh, rest = divmod(n, 100_000)
    thousand, below = divmod(rest, 1000)
    parts = []
    if lakh:
        parts.append(_below_hundred(lakh) + " lakh")
    if thousand:
        parts.append(_below_hundred(thousand) + " thousand")
    if below:
        parts.append(_below_thousand(below))
    return " ".join(parts)


def round_spoken(n: int) -> int:
    """Round so the number sounds like an estimate, not an invoice."""
    if n >= 100_000:
        return int(round(n / 5000) * 5000)
    if n >= 10_000:
        return int(round(n / 1000) * 1000)
    return int(round(n / 500) * 500)


def value_line(card_id: str, lead: dict) -> str:
    """One spoken sentence: what the card is roughly worth per year to THIS person. Empty if we have no spend band."""
    m = lead.get("monthly_category_spend_inr")
    if not m:
        return ""
    rupees, extra = _annual_value(card_id, int(m))
    rupees = round_spoken(rupees)
    if rupees <= 0:
        return ""
    cat = lead.get("spend_label") or lead.get("spend_hint", "everyday")
    if lead.get("relationship") == "existing":
        lead_in = f"Going by your {cat} spends with us, that's roughly"
    else:
        lead_in = f"On the {cat} spends you'd mentioned, that's roughly"
    tail = f" {extra}" if extra else ""
    return f"{lead_in} {rupees_in_words(rupees)} rupees back a year{tail}."


def personal_context(lead: dict) -> str:
    """What the agent may know and say about this person, in words it can use directly."""
    bits = []
    if lead.get("relationship") == "existing":
        if lead.get("tenure_years"):
            bits.append(f"{lead['customer_name']} has banked with us for about {rupees_in_words(int(lead['tenure_years']))} years")
        if lead.get("products_held"):
            bits.append(f"holds a {lead['products_held']} with the bank")
        if lead.get("monthly_category_spend_inr"):
            bits.append(f"the bank sees category-level spends on {lead.get('spend_hint', 'everyday spends')}, which is why this card was matched (only say this if asked how you know)")
    else:
        if lead.get("lead_source"):
            bits.append(f"lead source: {lead['lead_source']}")
        if lead.get("monthly_category_spend_inr"):
            bits.append(f"they declared their {lead.get('spend_hint', 'everyday')} spend at the source; you have no bank data on them")
    return "; ".join(bits) if bits else "nothing beyond the fields above"


def compose_hook(base_hook: str, lead: dict) -> str:
    """For new leads with a declared source, start the hook with why we are calling so it does not feel random."""
    src = lead.get("lead_source")
    if lead.get("relationship") == "existing" or not src:
        return base_hook
    return f"{src[0].upper()}{src[1:]}, and {base_hook[0].lower()}{base_hook[1:]}"


def fee_outlook(card: dict, lead: dict) -> str:
    """Honest, personalised answer to 'is it lifetime free?'.
    Voice of customer (r/IndianCreditCards): 'coupons plus a waiver so it is effectively LTF' is the line people call a scam.
    So: it is a paid card, here is the fee, the waiver is a condition THEY control, the voucher is a voucher, not a refund."""
    parts = [f"It's a paid card, {rupees_in_words(int(card['annual_fee_inr']))} rupees a year, I won't dress that up."]
    m = lead.get("monthly_category_spend_inr")
    waiver = card.get("fee_waiver_spend_inr")
    cat = lead.get("spend_label") or lead.get("spend_hint", "everyday")
    who = "with us" if lead.get("relationship") == "existing" else "you'd mentioned"
    if m and waiver:
        if int(m) * 12 >= waiver:
            parts.append(f"The waiver kicks in at {rupees_in_words(waiver)} of spend in the year; going by your {cat} spends {who} you'd likely cross it, and if you don't, you pay it.")
        else:
            parts.append(f"The waiver needs {rupees_in_words(waiver)} of spend in the year, and honestly on your {cat} spends {who} you may not get there, so count the fee as real.")
    elif waiver:
        parts.append(f"The waiver kicks in at {rupees_in_words(waiver)} of spend in the year.")
    if card.get("welcome_offsets_joining_fee"):
        parts.append(f"The welcome gift is {card.get('welcome_short') or card['welcome']}, same size as the joining fee, but it's a voucher, not a refund.")
    return " ".join(parts)


def limit_line(lead: dict) -> str:
    """Only for a genuine pre-approved existing customer: the concrete facts that make 'pre-approved' believable."""
    lim = lead.get("pre_approved_limit_inr")
    if not lim or lead.get("relationship") != "existing":
        return ""
    return f"The limit's already set at {rupees_in_words(int(lim))} rupees, you can see it in the app, and there's no documentation because the bank already has your KYC."


def offer_validity(lead: dict) -> str:
    till = lead.get("offer_valid_till")
    if not till or lead.get("relationship") != "existing":
        return ""
    return f"This pre-approved offer stays on your account till {till}, so there's no rush today, but it won't sit there forever."

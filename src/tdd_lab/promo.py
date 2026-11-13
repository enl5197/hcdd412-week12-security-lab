"""Promo-code pricing -- the feature you will build with TDD (Red-Green-Refactor).

Business rules (from the product owner):

* ``SAVE10``  - 10% off the subtotal (round the discount DOWN to a whole cent).
* ``FLAT5``   - $5.00 off, but only when the subtotal is at least $20.00.
* ``WELCOME`` - 15% off, valid only on or before 2026-12-31.
* Codes are case-insensitive and surrounding whitespace is ignored.
* An unknown, expired, or ineligible code must raise ``PromoError`` -- never
  silently return the full price.
* The total can never go below zero.

All money is integer cents. Dates are ``datetime.date``.

Right now this is only a stub. Write failing tests FIRST (Red), then make them
pass (Green), then clean up (Refactor).
"""
from datetime import date


class PromoError(ValueError):
    """Raised when a promo code cannot be applied."""


def apply_promo(subtotal_cents: int, code: str, today: date) -> int:
    if not isinstance(subtotal_cents, int) or isinstance(subtotal_cents, bool):
        raise PromoError("subtotal_cents must be an integer")
    if subtotal_cents < 0:
        raise PromoError("subtotal_cents cannot be negative")
    if not isinstance(today, date):
        raise PromoError("today must be a date")
    if code is None or not isinstance(code, str):
        raise PromoError("code must be a string")

    normalized_code = code.strip().upper()
    if not normalized_code:
        raise PromoError("code cannot be empty")

    if normalized_code == "SAVE10":
        discount = subtotal_cents * 10 // 100
        total = subtotal_cents - discount
    elif normalized_code == "FLAT5":
        if subtotal_cents < 2000:
            raise PromoError("FLAT5 requires subtotal >= $20.00")
        total = subtotal_cents - 500
    elif normalized_code == "WELCOME":
        if today > date(2026, 12, 31):
            raise PromoError("WELCOME has expired")
        discount = subtotal_cents * 15 // 100
        total = subtotal_cents - discount
    else:
        raise PromoError(f"unknown promo code: {code}")

    return max(0, total)


def test_rounds_discount_down():
# 10% of 1,005 is 100.5 -> discount rounds DOWN to 100 -> total 905
    assert apply_promo(1_005, "SAVE10", TODAY) == 905

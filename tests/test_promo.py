"""Your TDD workspace. The first test is deliberately RED -- that is step one."""
from datetime import date

import pytest

from tdd_lab.promo import PromoError, apply_promo

TODAY = date(2026, 11, 12)


def test_rounds_discount_down():
    # 10% of 1,005 is 100.5 -> discount rounds DOWN to 100 -> total 905
    assert apply_promo(1_005, "SAVE10", TODAY) == 905


def test_save10_takes_ten_percent_off():
    assert apply_promo(10_000, "SAVE10", TODAY) == 9_000


def test_flat5_requires_20_dollars_minimum():
    assert apply_promo(2_000, "FLAT5", TODAY) == 1_500
    with pytest.raises(PromoError):
        apply_promo(1_999, "FLAT5", TODAY)


def test_welcome_discount():
    assert apply_promo(10_000, "WELCOME", TODAY) == 8_500


def test_welcome_expiration_boundary():
    assert apply_promo(10_000, "WELCOME", date(2026, 12, 31)) == 8_500

    with pytest.raises(PromoError):
        apply_promo(10_000, "WELCOME", date(2027, 1, 1))


def test_code_ignores_case_and_whitespace():
    assert apply_promo(10_000, " save10 ", TODAY) == 9_000


def test_unknown_code_raises_error():
    with pytest.raises(PromoError):
        apply_promo(10_000, "INVALID", TODAY)


def test_total_never_goes_below_zero():
    assert apply_promo(0, "SAVE10", TODAY) == 0

# Next: write a failing test for the next rule, make it pass, refactor. Repeat.
# Think edge cases: rounding, case/whitespace, minimums, expiry date boundary,
# unknown code, and a total that would otherwise go negative.

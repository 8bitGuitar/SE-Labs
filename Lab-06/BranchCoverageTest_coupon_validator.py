import pytest
from coupon_validator import coupon_discount, best_discount, is_expired


# ---- coupon_discount: every decision True and False ----
@pytest.mark.parametrize("total", [0, -1])
def test_non_positive_cart_raises(total):
    with pytest.raises(ValueError, match="empty cart"):
        coupon_discount("WELCOME10", total, True, "mon")


def test_smallest_valid_cart_does_not_raise():
    assert coupon_discount("BOGUS", 0.01, False, "mon") == 0


@pytest.mark.parametrize("is_new_user, expected", [(True, 20), (False, 0)])
def test_welcome10(is_new_user, expected):
    assert coupon_discount("WELCOME10", 200, is_new_user, "mon") == expected


@pytest.mark.parametrize(
    "day, total, expected",
    [
        ("sat", 500, 100),    # weekend, boundary of >= 500
        ("sun", 1000, 200),   # weekend, large cart
        ("sat", 499, 50),     # weekend, just below boundary
        ("sun", 100, 50),     # weekend, small cart
        ("mon", 500, 0),      # weekday
        ("fri", 100, 0),      # weekday
    ],
)
def test_weekend20(day, total, expected):
    assert coupon_discount("WEEKEND20", total, False, day) == expected


@pytest.mark.parametrize("total, expected", [(301, 100), (300, 0), (299, 0), (1000, 100)])
def test_flat100(total, expected):
    assert coupon_discount("FLAT100", total, False, "mon") == expected


def test_unknown_code_returns_zero():
    assert coupon_discount("BOGUS", 100, True, "sat") == 0


def test_code_is_case_sensitive():
    assert coupon_discount("welcome10", 200, True, "mon") == 0


# ---- best_discount: loop entered / skipped, value > best both ways, cap both ways ----
def test_best_discount_no_codes():
    assert best_discount([], 100, True, "mon") == 0


def test_best_discount_new_best_replaces_lower():
    # WELCOME10 = 40, FLAT100 = 100 -> second value beats first
    assert best_discount(["WELCOME10", "FLAT100"], 400, True, "mon") == 100


def test_best_discount_keeps_earlier_when_later_is_not_higher():
    # FLAT100 = 100 first, WELCOME10 = 40 afterwards does not replace it
    assert best_discount(["FLAT100", "WELCOME10"], 400, True, "mon") == 100


def test_best_discount_equal_values_keep_first():
    assert best_discount(["FLAT100", "FLAT100"], 400, False, "mon") == 100


def test_best_discount_below_cap_returned_as_is():
    assert best_discount(["WELCOME10"], 200, True, "mon") == 20


def test_best_discount_exactly_at_cap_not_clipped():
    # WEEKEND20 flat 50 on a 125 cart: cap = 0.4 * 125 = 50.0, so best == cap
    assert best_discount(["WEEKEND20"], 125, False, "sat") == 50


def test_best_discount_clipped_to_cap():
    assert best_discount(["WEEKEND20"], 100, False, "sat") == pytest.approx(40)


def test_best_discount_all_codes_inapplicable():
    assert best_discount(["WELCOME10", "BOGUS"], 200, False, "mon") == 0


# ---- is_expired ----
@pytest.mark.parametrize("days_valid", [0, -5])
def test_non_positive_validity_is_expired(days_valid):
    assert is_expired(10, 5, days_valid) is True


@pytest.mark.parametrize(
    "today, start, days_valid, expected",
    [
        (20, 5, 10, True),    # elapsed 15 > 10
        (16, 5, 10, True),    # elapsed 11 > 10
        (15, 5, 10, False),   # elapsed 10 == 10, last valid day
        (5, 5, 10, False),    # same day
    ],
)
def test_expiry_window(today, start, days_valid, expected):
    assert is_expired(today, start, days_valid) is expected

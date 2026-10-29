import pytest
from coupon_validator import coupon_discount, best_discount, is_expired


# ---- coupon_discount: line coverage ----
def test_empty_cart_raises():
    with pytest.raises(ValueError, match="empty cart"):
        coupon_discount("WELCOME10", 0, True, "mon")


def test_welcome_coupon_new_user():
    assert coupon_discount("WELCOME10", 200, True, "mon") == 20


def test_welcome_coupon_existing_user():
    assert coupon_discount("WELCOME10", 200, False, "mon") == 0


def test_weekend_coupon_large_cart():
    assert coupon_discount("WEEKEND20", 500, False, "sat") == 100


def test_weekend_coupon_small_cart():
    assert coupon_discount("WEEKEND20", 200, False, "sun") == 50


def test_weekend_coupon_weekday():
    assert coupon_discount("WEEKEND20", 600, False, "mon") == 0


def test_flat100_large_cart():
    assert coupon_discount("FLAT100", 400, False, "mon") == 100


def test_flat100_small_cart():
    assert coupon_discount("FLAT100", 300, False, "mon") == 0


def test_unknown_code():
    assert coupon_discount("BOGUS", 100, False, "mon") == 0


# ---- best_discount: line coverage ----
def test_best_discount_picks_highest():
    assert best_discount(["WELCOME10", "FLAT100"], 400, True, "mon") == 100


def test_best_discount_capped_at_40_percent():
    # WEEKEND20 small-cart discount is 50, but the cap on a 100 cart is 40
    assert best_discount(["WEEKEND20"], 100, False, "sat") == 40


# ---- is_expired: line coverage ----
def test_zero_validity_expired():
    assert is_expired(10, 5, 0) is True


def test_expired_after_validity_window():
    assert is_expired(20, 5, 10) is True

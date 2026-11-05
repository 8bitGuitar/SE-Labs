from datetime import date

import pytest
from hypothesis import example, given, strategies as st
from coupon_validator import split_code, most_expensive, expiry_days

NOT_TEXT = st.integers() | st.floats() | st.booleans() | st.binary() | st.lists(st.text())


@given(st.text() | st.none())
def test_split_code_no_crash(s):
    try:
        split_code(s)
    except Exception as e:
        assert False, f"split_code crashed with: {e}"


@given(st.text() | st.none())
def test_most_expensive_no_crash(s):
    try:
        most_expensive(s)
    except Exception as e:
        assert False, f"most_expensive crashed with: {e}"


@given(st.text() | st.none())
def test_expiry_days_no_crash(s):
    try:
        expiry_days(s)
    except Exception as e:
        assert False, f"expiry_days crashed with: {e}"


@pytest.mark.parametrize("func", [split_code, most_expensive, expiry_days])
@given(value=NOT_TEXT)
def test_non_text_input_is_rejected(func, value):
    assert func(value) is None


# Text close to a real coupon code reaches deeper than purely random text.
@given(st.text(alphabet="abzAZ09-_ ٣ıß\n", max_size=12))
@example("save-" + "9" * 5000)
@example("ıs-1")
@example("save-٣")
@example("save-1_000")
def test_split_code_returns_clean_result_or_none(s):
    result = split_code(s)
    if result is not None:
        prefix, value = result
        assert prefix.isascii() and prefix.isalnum() and prefix == prefix.upper()
        assert isinstance(value, int) and value >= 0


@given(
    st.from_regex(r"[A-Za-z0-9]{1,10}", fullmatch=True),
    st.integers(min_value=0, max_value=999_999_999),
)
def test_split_code_accepts_valid_codes(prefix, value):
    assert split_code(f" {prefix}-{value} ") == (prefix.upper(), value)


GOOD_PRICES = ["10", "2.5", " 7 ", "0"]
BAD_PRICES = ["", "abc", "nan", "inf", "-inf", "-5", "1e999", "1_000", "٣", "9" * 400]


@given(st.lists(st.sampled_from(GOOD_PRICES + BAD_PRICES), min_size=1))
def test_most_expensive_rejects_any_bad_price(parts):
    expected = None
    if all(p in GOOD_PRICES for p in parts):
        expected = max(float(p) for p in parts)
    assert most_expensive(",".join(parts)) == expected


@given(st.lists(st.floats(min_value=0, max_value=1e9), min_size=1))
def test_most_expensive_finds_the_highest_price(prices):
    parts = [f"{p:.2f}" for p in prices]
    assert most_expensive(",".join(parts)) == max(float(p) for p in parts)


@given(
    st.integers(min_value=0, max_value=9999),
    st.integers(min_value=-1, max_value=40),
    st.integers(min_value=-1, max_value=40),
)
def test_expiry_days_only_accepts_real_dates(year, month, day):
    try:
        date(year, month, day)
        is_real = True
    except ValueError:
        is_real = False
    result = expiry_days(f"{year:04d}-{month}-{day}")
    assert (result is not None) == is_real


@given(st.dates())
def test_expiry_days_formula_for_valid_dates(d):
    expected = (d.year - 2024) * 365 + (d.month - 1) * 30 + d.day
    assert expiry_days(d.isoformat()) == expected

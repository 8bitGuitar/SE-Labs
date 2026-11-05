import math
import re
from datetime import date

CODE_PATTERN = re.compile(r"([A-Za-z0-9]+)-([0-9]{1,9})")
PRICE_PATTERN = re.compile(r"[0-9]+(\.[0-9]*)?|\.[0-9]+")
DATE_PATTERN = re.compile(r"([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})")

def split_code(code):
    if not isinstance(code, str):
        return None
    match = CODE_PATTERN.fullmatch(code.strip())
    if match is None:
        return None
    return match.group(1).upper(), int(match.group(2))

def most_expensive(prices_csv):
    if not isinstance(prices_csv, str):
        return None
    parts = [p.strip() for p in prices_csv.split(',')]
    if not all(PRICE_PATTERN.fullmatch(p) for p in parts):
        return None
    prices = [float(p) for p in parts]
    if not all(math.isfinite(p) for p in prices):
        return None
    return max(prices)

def expiry_days(date_text):
    if not isinstance(date_text, str):
        return None
    match = DATE_PATTERN.fullmatch(date_text.strip())
    if match is None:
        return None
    year, month, day = [int(p) for p in match.groups()]
    try:
        date(year, month, day)
    except ValueError:
        return None
    return (year - 2024) * 365 + (month - 1) * 30 + day

def main():
    print("==== Running split_code ====")
    user_input = input("Enter a coupon code (e.g. save-20): ")
    result = split_code(user_input)
    if result is None:
        print("Invalid coupon code")
    else:
        print("Prefix and Value:", result)

    print("\n==== Running most_expensive ====")
    user_input = input("Enter item prices as CSV (e.g. 199,49.5,320): ")
    result = most_expensive(user_input)
    if result is None:
        print("Invalid price list")
    else:
        print("Most Expensive Item:", result)

    print("\n==== Running expiry_days ====")
    user_input = input("Enter an expiry date as YYYY-MM-DD: ")
    result = expiry_days(user_input)
    if result is None:
        print("Invalid expiry date")
    else:
        print("Days Since 2024:", result)

if __name__ == "__main__":
    main()

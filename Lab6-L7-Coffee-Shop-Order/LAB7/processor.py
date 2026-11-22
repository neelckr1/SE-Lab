import math

def lookup_drink_code(code_string):
    """
    Looks up base drink price by prefix (first 3 letters, case-insensitive).
    Returns base price (float) if recognized, or None if invalid or not found.
    """
    if not isinstance(code_string, str):
        return None
    cleaned = code_string.strip()
    if not cleaned:
        return None
    code_prefix = cleaned[:3].upper()
    menu_prices = {
        "LAT": 4.50,
        "CAP": 4.00,
        "ESP": 3.00,
        "AME": 3.50,
        "MOC": 5.00  # Fixed 'MOc' bug to standardized uppercase 'MOC'
    }
    return menu_prices.get(code_prefix, None)

def calculate_average_shot_cost(pricing_csv):
    """
    Calculates average shot cost from a comma-separated numeric string.
    Safely ignores whitespace, invalid numeric tokens, NaNs, and negative values.
    Returns average (float), or 0.0 if no valid prices are present.
    """
    if not isinstance(pricing_csv, str):
        return 0.0
    prices = []
    for p in pricing_csv.split(','):
        token = p.strip()
        if not token:
            continue
        try:
            val = float(token)
            if math.isnan(val) or math.isinf(val) or val < 0:
                continue
            prices.append(val)
        except ValueError:
            continue
    if not prices:
        return 0.0
    return sum(prices) / len(prices)

def parse_order_modifiers(order_spec):
    """
    Parses semicolon-separated key:value modifier specifications.
    Safely handles malformed entries, missing colons, multiple colons, and whitespace.
    Returns a dictionary of cleaned modifiers.
    """
    if not isinstance(order_spec, str):
        return {}
    modifier_dict = {}
    for item in order_spec.split(';'):
        item = item.strip()
        if not item or ':' not in item:
            continue
        key, value = item.split(':', 1)
        k_clean = key.strip()
        v_clean = value.strip()
        if k_clean:
            modifier_dict[k_clean] = v_clean
    return modifier_dict

def main():
    print("==== Running lookup_drink_code ====")
    drink_input = input("Enter drink code prefix (e.g. LAT, CAP, ESP): ")
    price = lookup_drink_code(drink_input)
    if price is not None:
        print(f"Base Price: ${price:.2f}")
    else:
        print(f"Base Price: Invalid drink code '{drink_input}' (Not Found / Unrecognized)")

    print("\n==== Running calculate_average_shot_cost ====")
    shots_input = input("Enter CSV of shot prices (e.g. 1.0, 1.5, 2.0): ")
    avg_price = calculate_average_shot_cost(shots_input)
    print(f"Average Shot Price: ${avg_price:.2f}")

    print("\n==== Running parse_order_modifiers ====")
    spec_input = input("Enter modifiers (e.g. milk:oat;syrup:vanilla): ")
    mods = parse_order_modifiers(spec_input)
    print("Parsed Modifiers:", mods)

if __name__ == "__main__":
    main()

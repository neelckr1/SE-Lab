from hypothesis import given, strategies as st
from processor import lookup_drink_code, calculate_average_shot_cost, parse_order_modifiers

@given(st.text() | st.none())
def test_lookup_drink_code_no_crash(s):
    try:
        lookup_drink_code(s)
    except Exception as e:
        assert False, f"lookup_drink_code crashed with: {e}"

@given(st.text() | st.none())
def test_calculate_average_shot_cost_safe(s):
    try:
        calculate_average_shot_cost(s)
    except Exception as e:
        assert False, f"calculate_average_shot_cost crashed with: {e}"

@given(st.text() | st.none())
def test_parse_order_modifiers_safe(s):
    try:
        parse_order_modifiers(s)
    except Exception as e:
        assert False, f"parse_order_modifiers crashed with: {e}"

# Additional targeted fuzzing strategies
@given(st.sampled_from(["LAT", "CAP", "ESP", "AME", "MOc", "MOC", "lat", "cap", "esp", "ame", "moc", "xyz", "EXTRA", "", "  ", None]))
def test_lookup_drink_code_categories(code):
    try:
        result = lookup_drink_code(code)
        if code in ["LAT", "CAP", "ESP", "AME", "MOc", "MOC", "lat", "cap", "esp", "ame", "moc"]:
            # Valid code prefixes should return float price
            assert isinstance(result, (float, int))
        else:
            # Invalid code prefixes should safely return None
            assert result is None
    except Exception as e:
        assert False, f"lookup_drink_code crashed on '{code}' with: {e}"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False, min_value=0.0, max_value=100.0), max_size=5))
def test_calculate_average_shot_cost_numeric(prices):
    csv_str = ", ".join(f"{p:.2f}" for p in prices)
    try:
        avg = calculate_average_shot_cost(csv_str)
        if len(prices) > 0:
            expected = sum(round(p, 2) for p in prices) / len(prices)
            assert abs(avg - expected) < 1e-2
        else:
            assert avg == 0.0
    except Exception as e:
        assert False, f"calculate_average_shot_cost crashed on '{csv_str}' with: {e}"

@given(st.lists(st.tuples(st.text(alphabet="abcdefghijklmnopqrstuvwxyz", min_size=1, max_size=8), 
                          st.text(alphabet="abcdefghijklmnopqrstuvwxyz", min_size=1, max_size=8)), max_size=5))
def test_parse_order_modifiers_delimiters(pairs):
    order_str = ";".join(f"{k}:{v}" for k, v in pairs)
    try:
        res = parse_order_modifiers(order_str)
        assert isinstance(res, dict)
    except Exception as e:
        assert False, f"parse_order_modifiers crashed on '{order_str}' with: {e}"

"""
Energy Consumption and Tariff Calculator Module.

This module provides utility functions to record electricity meter readings,
compute tiered utility bills, detect consumption spikes, and persist meter
data into JSON storage.
"""

from datetime import datetime
import json
from typing import Dict, List, Optional, Tuple

# Module Constants
DEFAULT_TIER_1_RATE = 3.5
DEFAULT_TIER_2_RATE = 5.0
DEFAULT_TIER_3_RATE = 7.5
SPIKE_LIMIT = 500

# Mutable state container avoiding Pylint W0603 (global-statement)
SYSTEM_STATE: Dict[str, object] = {
    "meters": {},
    "tier_rates": [
        DEFAULT_TIER_1_RATE,
        DEFAULT_TIER_2_RATE,
        DEFAULT_TIER_3_RATE,
    ],
}


def get_meters() -> Dict[str, float]:
    """Return the dictionary of meter IDs mapped to cumulative units."""
    return SYSTEM_STATE["meters"]  # type: ignore[return-value]


def get_rates() -> List[float]:
    """Return a copy of the current three-tier electricity rates."""
    rates = SYSTEM_STATE["tier_rates"]
    return list(rates)  # type: ignore[arg-type]


def record_reading(
    meter_id: str,
    units: float,
    history: Optional[List[Tuple[str, float, str]]] = None,
) -> List[Tuple[str, float, str]]:
    """Record a meter reading with timestamp and update cumulative usage.

    Args:
        meter_id: Unique identifier for the utility meter.
        units: Number of kilowatt-hours consumed.
        history: Optional list tracking reading history tuples.

    Returns:
        Updated reading history list.
    """
    if history is None:
        history = []

    if units < 0:
        print(
            f"Warning: Negative consumption {units} for {meter_id} recorded."
        )

    timestamp = str(datetime.now())
    history.append((meter_id, units, timestamp))

    meters = get_meters()
    meters[meter_id] = meters.get(meter_id, 0.0) + units
    return history


def compute_bill(meter_id: str, tier_rates: List[float]) -> float:
    """Compute the tiered electricity bill for a given meter ID.

    Tariff Structure:
        - Tier 1: First 100 units at tier_rates[0]
        - Tier 2: Next 200 units (101-300) at tier_rates[1]
        - Tier 3: Consumption above 300 units at tier_rates[2]

    Args:
        meter_id: Identifier of the meter to calculate the bill for.
        tier_rates: A list of 3 float rates corresponding to tiers 1, 2, and 3.

    Returns:
        The total bill amount as a float.
    """
    meters = get_meters()
    units = meters.get(meter_id, 0.0)

    if units <= 100:
        return units * tier_rates[0]

    if units <= 300:
        return 100 * tier_rates[0] + (units - 100) * tier_rates[1]

    return (
        100 * tier_rates[0]
        + 200 * tier_rates[1]
        + (units - 300) * tier_rates[2]
    )


def raise_rates(percent: float) -> None:
    """Increase all tariff tier rates by a given percentage.

    Args:
        percent: Percentage increase to apply to each tier.
    """
    rates: List[float] = SYSTEM_STATE["tier_rates"]  # type: ignore[assignment]
    multiplier = 1.0 + (percent / 100.0)
    for idx, rate in enumerate(rates):
        rates[idx] = rate * multiplier


def flag_spikes(limit: float = SPIKE_LIMIT) -> List[str]:
    """Identify meter IDs whose recorded consumption exceeds the spike limit.

    Args:
        limit: Threshold above which consumption is considered an anomaly.

    Returns:
        List of meter IDs that exceeded the limit.
    """
    meters = get_meters()
    return [m_id for m_id, usage in meters.items() if usage > limit]


def load_meter_data(file: str = "meters.json") -> None:
    """Load persisted meter consumption data from a JSON file.

    Args:
        file: Path to the JSON file containing meter readings.
    """
    meters = get_meters()
    try:
        with open(file, "r", encoding="utf-8") as file_handle:
            data = json.loads(file_handle.read())
            meters.clear()
            meters.update(data)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        meters.clear()


def save_meter_data(file: str = "meters.json") -> None:
    """Persist current meter consumption data to a JSON file.

    Args:
        file: Destination path for the saved JSON file.
    """
    meters = get_meters()
    with open(file, "w", encoding="utf-8") as file_handle:
        file_handle.write(json.dumps(meters, indent=2))


def safe_parse_expression(expr_str: str) -> float:
    """Safely parse a numerical adjustment string without using eval.

    Args:
        expr_str: User input string representing numeric adjustment.

    Returns:
        Float value of the adjustment, defaulting to 0.0 on invalid input.
    """
    clean_str = expr_str.strip()
    if not clean_str:
        return 0.0

    try:
        parts = clean_str.split("+")
        return sum(float(part.strip()) for part in parts)
    except ValueError:
        print(f"Warning: Invalid adjustment expression '{expr_str}'. Using 0.")
        return 0.0


def main() -> None:
    """Main execution workflow demonstrating energy system functionality."""
    history: List[Tuple[str, float, str]] = []
    record_reading("M-01", 120, history)
    record_reading("M-02", 640, history)
    record_reading("M-03", -50, history)
    print(f"Readings stored so far: {len(history)}")

    raise_rates(10)
    rates = get_rates()

    print(f"Bill M-01: {compute_bill('M-01', rates):.2f}")
    print(f"Bill M-03: {compute_bill('M-03', rates):.2f}")
    print(f"Spikes: {flag_spikes()}")

    prompt = "Extra units for M-01 as an expression (Enter for 0): "
    adjustment_input = input(prompt) or "0"
    adjustment_val = safe_parse_expression(adjustment_input)

    record_reading("M-01", adjustment_val, history)
    save_meter_data()
    load_meter_data()
    print(f"Bill M-01 after reload: {compute_bill('M-01', rates):.2f}")


if __name__ == "__main__":
    main()

import pytest
from coffee_shop_order import process_order_batch, check_espresso_machine


# =====================================================================
# Tests for process_order_batch
# =====================================================================

def test_invalid_orders_type_raises_value_error():
    """Invalid orders argument (not a list) raises ValueError."""
    with pytest.raises(ValueError, match="Invalid orders list or tax rate"):
        process_order_batch("not_a_list", 0.05)


def test_negative_tax_rate_raises_value_error():
    """Negative tax rate raises ValueError."""
    with pytest.raises(ValueError, match="Invalid orders list or tax rate"):
        process_order_batch([], -0.05)


def test_unpaid_order_skipped():
    """Unpaid orders should be skipped."""
    orders = [
        {"paid": False, "size": "small"},
        {"paid": True, "size": "small", "is_member": False}
    ]
    result = process_order_batch(orders, 0.0)
    assert result["total"] == 3.0
    assert result["status"] == "COMPLETED"


def test_sizes_and_pricing():
    """Small, medium, and large sizes calculate correct base prices."""
    orders = [
        {"paid": True, "size": "small"},
        {"paid": True, "size": "medium"},
        {"paid": True, "size": "large"}
    ]
    result = process_order_batch(orders, 0.0)
    # small=3.0 + medium=4.5 + large=6.0 = 13.5
    assert result["total"] == 13.5
    assert result["status"] == "COMPLETED"


def test_invalid_size_rejected():
    """Invalid drink size increments rejected_items and skips the order."""
    orders = [
        {"paid": True, "size": "extra_large"},
        {"paid": True, "size": "medium"}
    ]
    result = process_order_batch(orders, 0.0)
    assert result["total"] == 4.5
    assert result["status"] == "COMPLETED"


def test_customization_negative_cost_rejected():
    """Negative customization cost increments rejected_items and skips modification."""
    orders = [
        {
            "paid": True,
            "size": "medium",
            "customizations": [
                {"type": "syrup", "cost": -1.0},
                {"type": "syrup", "cost": 0.5}
            ]
        }
    ]
    result = process_order_batch(orders, 0.0)
    # medium=4.5 + syrup=0.5 = 5.0
    assert result["total"] == 5.0
    assert result["status"] == "COMPLETED"


def test_allergen_alert_with_strict_allergy():
    """Allergen alert with strict_allergy zeroes item_total and stops customizations."""
    orders = [
        {
            "paid": True,
            "size": "medium",
            "strict_allergy": True,
            "customizations": [
                {"type": "allergen_alert", "cost": 0.0},
                {"type": "syrup", "cost": 0.5}  # should not be added due to break
            ]
        }
    ]
    result = process_order_batch(orders, 0.0)
    assert result["total"] == 0.0
    assert result["status"] == "NO_SALE"


def test_allergen_alert_without_strict_allergy():
    """Allergen alert without strict_allergy records rejection but continues."""
    orders = [
        {
            "paid": True,
            "size": "medium",
            "strict_allergy": False,
            "customizations": [
                {"type": "allergen_alert", "cost": 0.0},
                {"type": "syrup", "cost": 0.5}
            ]
        }
    ]
    result = process_order_batch(orders, 0.0)
    # medium=4.5 + syrup=0.5 = 5.0
    assert result["total"] == 5.0
    assert result["status"] == "COMPLETED"


def test_syrup_cost_capping():
    """Syrup costs above 1.5 are capped at 1.5; costs <= 1.5 are preserved."""
    orders = [
        {
            "paid": True,
            "size": "small",  # 3.0
            "customizations": [{"type": "syrup", "cost": 2.5}]  # capped at 1.5 -> 4.5
        },
        {
            "paid": True,
            "size": "small",  # 3.0
            "customizations": [{"type": "syrup", "cost": 1.2}]  # 1.2 -> 4.2
        }
    ]
    result = process_order_batch(orders, 0.0)
    assert result["total"] == 8.7
    assert result["status"] == "COMPLETED"


def test_standard_customization_and_member_discount():
    """Standard modifications add cost, and member receives 10% discount."""
    orders = [
        {
            "paid": True,
            "size": "small",  # 3.0
            "is_member": True,
            "customizations": [{"type": "extra_shot", "cost": 1.0}]  # total=4.0 -> * 0.90 = 3.6
        }
    ]
    result = process_order_batch(orders, 0.1)  # 3.6 * 1.1 = 3.96
    assert result["total"] == 3.96
    assert result["status"] == "COMPLETED"


def test_audit_rejected_when_more_than_four_rejections():
    """More than 4 rejected items trigger AUDIT_REJECTED."""
    orders = [
        {"paid": True, "size": "invalid_1"},
        {"paid": True, "size": "invalid_2"},
        {"paid": True, "size": "invalid_3"},
        {"paid": True, "size": "invalid_4"},
        {"paid": True, "size": "invalid_5"},
        {"paid": True, "size": "small"}  # 3.0
    ]
    result = process_order_batch(orders, 0.0)
    assert result["status"] == "AUDIT_REJECTED"
    assert result["total"] == 3.0


def test_no_sale_when_batch_total_is_zero():
    """When batch total is zero, status is NO_SALE."""
    orders = []
    result = process_order_batch(orders, 0.1)
    assert result["total"] == 0.0
    assert result["status"] == "NO_SALE"


# =====================================================================
# Tests for check_espresso_machine
# =====================================================================

def test_espresso_machine_no_data():
    """Empty or falsy temperature cycles return NO_DATA."""
    assert check_espresso_machine([]) == "NO_DATA"
    assert check_espresso_machine(None) == "NO_DATA"


def test_espresso_machine_shutdown_on_consecutive_overheat():
    """Two consecutive readings above 96.0 trigger SHUTDOWN."""
    cycles = [
        [92.0, 97.5, 98.2, 90.0]
    ]
    assert check_espresso_machine(cycles) == "SHUTDOWN"


def test_espresso_machine_optimal_with_streak_reset():
    """Overheating that is interrupted by a normal temp resets streak and returns OPTIMAL."""
    cycles = [
        [97.0, 95.0, 97.0, 94.0],
        [90.0, 91.0]
    ]
    assert check_espresso_machine(cycles) == "OPTIMAL"

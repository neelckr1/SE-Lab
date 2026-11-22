import pytest
from coffee_shop_order import process_order_batch, check_espresso_machine


# =====================================================================
# Branch Coverage Tests for process_order_batch
# =====================================================================

class TestProcessOrderBatchBranchCoverage:
    """
    Branch coverage test suite designed to evaluate all decision paths,
    boolean conditions, and boundary conditions to True and False.
    """

    def test_branch_validation_orders_not_list(self):
        """Branch: not isinstance(orders, list) evaluates to True."""
        with pytest.raises(ValueError, match="Invalid orders list or tax rate"):
            process_order_batch("invalid_string", 0.05)

        with pytest.raises(ValueError, match="Invalid orders list or tax rate"):
            process_order_batch({"not": "a list"}, 0.05)

    def test_branch_validation_tax_rate_negative(self):
        """Branch: not isinstance(orders, list) is False, but tax_rate < 0 is True."""
        with pytest.raises(ValueError, match="Invalid orders list or tax rate"):
            process_order_batch([], -0.01)

    def test_branch_validation_valid_inputs(self):
        """Branch: both conditions in validation evaluate to False (passes check)."""
        result = process_order_batch([], 0.0)
        assert result["status"] == "NO_SALE"

    def test_branch_unpaid_order(self):
        """
        Branch: not order.get('paid', False)
        - Case 1: 'paid' is explicitly False -> skips order
        - Case 2: 'paid' key is omitted (defaults to False) -> skips order
        """
        orders = [
            {"paid": False, "size": "small"},
            {"size": "small"}  # missing 'paid'
        ]
        result = process_order_batch(orders, 0.05)
        assert result["total"] == 0.0
        assert result["status"] == "NO_SALE"

    def test_branch_paid_order(self):
        """Branch: not order.get('paid', False) is False -> order is processed."""
        orders = [{"paid": True, "size": "small"}]
        result = process_order_batch(orders, 0.0)
        assert result["total"] == 3.0
        assert result["status"] == "COMPLETED"

    def test_branch_drink_sizes_all_paths(self):
        """
        Branches: size == 'small', 'medium', 'large', and else (invalid size).
        Also tests omitted 'size' defaulting to 'medium'.
        """
        # Test size == 'small'
        res_small = process_order_batch([{"paid": True, "size": "small"}], 0.0)
        assert res_small["total"] == 3.0

        # Test size == 'medium'
        res_med = process_order_batch([{"paid": True, "size": "medium"}], 0.0)
        assert res_med["total"] == 4.5

        # Test default size when omitted -> 'medium'
        res_default = process_order_batch([{"paid": True}], 0.0)
        assert res_default["total"] == 4.5

        # Test size == 'large'
        res_large = process_order_batch([{"paid": True, "size": "large"}], 0.0)
        assert res_large["total"] == 6.0

        # Test invalid size -> increments rejected_items and continues
        res_invalid = process_order_batch([{"paid": True, "size": "venti"}], 0.0)
        assert res_invalid["total"] == 0.0
        assert res_invalid["status"] == "NO_SALE"

    def test_branch_customizations_cost_negative(self):
        """Branch: cost < 0 evaluates to True (rejected) vs False (processed)."""
        orders = [
            {
                "paid": True,
                "size": "small",  # 3.0
                "customizations": [
                    {"type": "flavor", "cost": -0.5},  # rejected (< 0)
                    {"type": "flavor", "cost": 0.5}    # accepted (>= 0)
                ]
            }
        ]
        result = process_order_batch(orders, 0.0)
        # 3.0 + 0.5 = 3.5
        assert result["total"] == 3.5
        assert result["status"] == "COMPLETED"

    def test_branch_allergen_alert_with_strict_allergy(self):
        """
        Branch: mod_type == 'allergen_alert' (True)
        AND order.get('strict_allergy', False) (True) -> item_total=0.0, breaks loop.
        """
        orders = [
            {
                "paid": True,
                "size": "large",  # 6.0
                "strict_allergy": True,
                "customizations": [
                    {"type": "allergen_alert", "cost": 0.0},
                    {"type": "extra_shot", "cost": 1.0}  # skipped due to break
                ]
            }
        ]
        result = process_order_batch(orders, 0.0)
        assert result["total"] == 0.0
        assert result["status"] == "NO_SALE"

    def test_branch_allergen_alert_without_strict_allergy(self):
        """
        Branch: mod_type == 'allergen_alert' (True)
        AND order.get('strict_allergy', False) (False) -> does not zero item_total, does not break.
        """
        orders = [
            {
                "paid": True,
                "size": "small",  # 3.0
                "strict_allergy": False,
                "customizations": [
                    {"type": "allergen_alert", "cost": 0.0},
                    {"type": "extra_shot", "cost": 1.0}  # processed
                ]
            }
        ]
        result = process_order_batch(orders, 0.0)
        # 3.0 + 1.0 = 4.0
        assert result["total"] == 4.0
        assert result["status"] == "COMPLETED"

    def test_branch_syrup_pricing_boundary(self):
        """
        Branch: mod_type == 'syrup'
        Ternary branch: cost if cost <= 1.5 else 1.5
        - Test cost <= 1.5 (e.g. 1.0 and exactly 1.5)
        - Test cost > 1.5 (e.g. 2.0 capped at 1.5)
        """
        orders = [
            {
                "paid": True,
                "size": "small",  # 3.0
                "customizations": [{"type": "syrup", "cost": 1.5}]  # 1.5 boundary -> +1.5 = 4.5
            },
            {
                "paid": True,
                "size": "small",  # 3.0
                "customizations": [{"type": "syrup", "cost": 2.5}]  # >1.5 capped -> +1.5 = 4.5
            },
            {
                "paid": True,
                "size": "small",  # 3.0
                "customizations": [{"type": "syrup", "cost": 0.75}]  # <1.5 -> +0.75 = 3.75
            }
        ]
        result = process_order_batch(orders, 0.0)
        # 4.5 + 4.5 + 3.75 = 12.75
        assert result["total"] == 12.75
        assert result["status"] == "COMPLETED"

    def test_branch_customization_general_else(self):
        """Branch: mod_type not allergen_alert and not syrup (hits else block)."""
        orders = [
            {
                "paid": True,
                "size": "small",  # 3.0
                "customizations": [{"type": "oat_milk", "cost": 0.75}]
            }
        ]
        result = process_order_batch(orders, 0.0)
        assert result["total"] == 3.75

    def test_branch_member_discount_true_and_false(self):
        """
        Branch: order.get('is_member', False)
        - Case 1: is_member=True -> applies 10% discount
        - Case 2: is_member=False -> no discount
        """
        order_member = [{"paid": True, "size": "large", "is_member": True}]  # 6.0 * 0.90 = 5.40
        order_non_member = [{"paid": True, "size": "large", "is_member": False}]  # 6.0

        res_member = process_order_batch(order_member, 0.0)
        res_non_member = process_order_batch(order_non_member, 0.0)

        assert res_member["total"] == 5.40
        assert res_non_member["total"] == 6.0

    def test_branch_audit_rejected_boundary(self):
        """
        Branch: rejected_items > 4
        - Case 1: rejected_items == 4 (boundary: does not trigger AUDIT_REJECTED)
        - Case 2: rejected_items == 5 (boundary + 1: triggers AUDIT_REJECTED)
        """
        # 4 rejections (not > 4) -> should be COMPLETED
        orders_4_rejections = [
            {"paid": True, "size": "bad1"},
            {"paid": True, "size": "bad2"},
            {"paid": True, "size": "bad3"},
            {"paid": True, "size": "bad4"},
            {"paid": True, "size": "small"}  # 3.0
        ]
        res_4 = process_order_batch(orders_4_rejections, 0.0)
        assert res_4["status"] == "COMPLETED"
        assert res_4["total"] == 3.0

        # 5 rejections (> 4) -> should be AUDIT_REJECTED
        orders_5_rejections = [
            {"paid": True, "size": "bad1"},
            {"paid": True, "size": "bad2"},
            {"paid": True, "size": "bad3"},
            {"paid": True, "size": "bad4"},
            {"paid": True, "size": "bad5"},
            {"paid": True, "size": "small"}  # 3.0
        ]
        res_5 = process_order_batch(orders_5_rejections, 0.0)
        assert res_5["status"] == "AUDIT_REJECTED"
        assert res_5["total"] == 3.0

    def test_branch_status_no_sale_vs_completed(self):
        """
        Branch: batch_total == 0.0 (NO_SALE) vs batch_total > 0.0 (COMPLETED)
        """
        res_no_sale = process_order_batch([], 0.1)
        assert res_no_sale["status"] == "NO_SALE"
        assert res_no_sale["total"] == 0.0

        res_completed = process_order_batch([{"paid": True, "size": "small"}], 0.1)
        assert res_completed["status"] == "COMPLETED"
        assert res_completed["total"] == 3.3  # 3.0 * 1.1


# =====================================================================
# Branch Coverage Tests for check_espresso_machine
# =====================================================================

class TestCheckEspressoMachineBranchCoverage:
    """
    Branch coverage test suite for temperature monitoring cycles and overheat shutdown.
    """

    def test_branch_no_temperature_data(self):
        """
        Branch: not temperature_cycles
        - Case 1: empty list [] -> True
        - Case 2: None -> True
        """
        assert check_espresso_machine([]) == "NO_DATA"
        assert check_espresso_machine(None) == "NO_DATA"

    def test_branch_empty_cycle(self):
        """
        Branch: cycle has no readings, outer loop runs but inner loop doesn't.
        """
        assert check_espresso_machine([[]]) == "OPTIMAL"

    def test_branch_shutdown_two_consecutive_overheats(self):
        """
        Branch: temp > 96.0 evaluates to True, and overheat_streak >= 2 evaluates to True.
        Immediate return 'SHUTDOWN'.
        """
        cycles = [
            [94.0, 96.5, 97.2, 91.0]
        ]
        assert check_espresso_machine(cycles) == "SHUTDOWN"

    def test_branch_single_overheat_does_not_shutdown(self):
        """
        Branch: temp > 96.0 is True (streak=1, not >= 2), then temp <= 96.0 is True (resets streak to 0).
        """
        cycles = [
            [96.1, 95.9, 96.2, 95.0]  # Isolated overheat readings interspersed with normal readings
        ]
        assert check_espresso_machine(cycles) == "OPTIMAL"

    def test_branch_boundary_temp_exactly_96(self):
        """
        Branch: boundary at temp == 96.0 (not > 96.0, evaluates to else branch, resetting streak).
        """
        cycles = [
            [96.0, 96.0, 96.0]
        ]
        assert check_espresso_machine(cycles) == "OPTIMAL"

    def test_branch_multiple_cycles_optimal(self):
        """
        Branch: multiple cycles evaluated without triggering shutdown -> returns 'OPTIMAL'.
        """
        cycles = [
            [90.0, 92.5, 91.0],
            [93.0, 94.0, 95.0]
        ]
        assert check_espresso_machine(cycles) == "OPTIMAL"

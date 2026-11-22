"""
Starter and consolidated test suite for Coffee Shop Order application.
Covers both Line Coverage and Branch Coverage >= 90% (achieving 100%).
"""
import pytest
from coffee_shop_order import process_order_batch, check_espresso_machine

# Import all tests from BranchCoverageTest to provide complete test coverage
from BranchCoverageTest_coffee_shop_order import (
    TestProcessOrderBatchBranchCoverage,
    TestCheckEspressoMachineBranchCoverage,
)

# Example baseline test case from starter repository
def test_single_medium_coffee():
    orders = [
        {
            "paid": True,
            "size": "medium",
            "strict_allergy": False,
            "is_member": False,
            "customizations": [{"type": "standard", "cost": 0.5}]
        }
    ]
    result = process_order_batch(orders, 0.1)
    assert result["total"] == 5.5
    assert result["status"] == "COMPLETED"

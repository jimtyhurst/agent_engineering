import pytest
from unittest.mock import MagicMock
from order_service import (
    Order,
    InventoryService,
    PaymentGateway,
    InventoryShortageError,
    PaymentFailedError,
    InvalidOrderError
)


@pytest.fixture
def mock_inventory():
    """Fixture to create a mock InventoryService."""
    return MagicMock(spec=InventoryService)


@pytest.fixture
def mock_payment():
    """Fixture to create a mock PaymentGateway."""
    return MagicMock(spec=PaymentGateway)


@pytest.fixture
def order(mock_inventory, mock_payment):
    """Fixture to create a default non-VIP order."""
    return Order(
        inventory_service=mock_inventory,
        payment_gateway=mock_payment,
        customer_email="test@example.com",
        is_vip=False
    )


@pytest.fixture
def vip_order(mock_inventory, mock_payment):
    """Fixture to create a VIP order."""
    return Order(
        inventory_service=mock_inventory,
        payment_gateway=mock_payment,
        customer_email="vip@example.com",
        is_vip=True
    )


# --- 1. Cart Management Tests ---

def test_add_item_success(order):
    order.add_item("item-1", 15.0, 2)
    assert "item-1" in order.items
    assert order.items["item-1"] == {"price": 15.0, "qty": 2}


def test_add_item_increment_quantity(order):
    order.add_item("item-1", 10.0, 1)
    order.add_item("item-1", 10.0, 3)
    assert order.items["item-1"]["qty"] == 4


def test_add_item_negative_price(order):
    with pytest.raises(ValueError, match="Price cannot be negative"):
        order.add_item("item-1", -5.0, 1)


def test_add_item_invalid_quantity(order):
    with pytest.raises(ValueError, match="Quantity must be greater than zero"):
        order.add_item("item-1", 10.0, 0)
    
    with pytest.raises(ValueError, match="Quantity must be greater than zero"):
        order.add_item("item-1", 10.0, -2)


def test_remove_item(order):
    order.add_item("item-1", 10.0, 1)
    order.add_item("item-2", 20.0, 1)
    
    order.remove_item("item-1")
    assert "item-1" not in order.items
    assert "item-2" in order.items


def test_remove_nonexistent_item_does_not_error(order):
    order.remove_item("nonexistent-item")  # Should not raise exception


# --- 2. Discount & Total Price Logic Tests ---

def test_total_price_calculation(order):
    order.add_item("item-1", 20.0, 2)  # 40.0
    order.add_item("item-2", 30.0, 1)  # 30.0
    assert order.total_price == 70.0


def test_apply_discount_regular_under_threshold(order):
    order.add_item("item-1", 50.0, 1)  # $50 total (<= $100)
    assert order.apply_discount() == 50.0  # No discount


def test_apply_discount_regular_over_threshold(order):
    order.add_item("item-1", 60.0, 2)  # $120 total (> $100)
    # 10% discount on $120 = $108.00
    assert order.apply_discount() == 108.00


def test_apply_discount_vip_always_20_percent(vip_order):
    vip_order.add_item("item-1", 50.0, 1)  # $50 total (under $100)
    # VIP flat 20% discount on $50 = $40.00
    assert vip_order.apply_discount() == 40.00

    vip_order.items.clear()
    vip_order.add_item("item-1", 200.0, 1)  # $200 total (over $100)
    # VIP flat 20% discount on $200 = $160.00
    assert vip_order.apply_discount() == 160.00


# --- 3. Checkout Workflow & Mock Verification Tests ---

def test_checkout_empty_cart_raises_invalid_order_error(order):
    with pytest.raises(InvalidOrderError, match="Cannot checkout an empty cart"):
        order.checkout()


def test_checkout_insufficient_stock(order, mock_inventory, mock_payment):
    order.add_item("prod-A", 25.0, 3)
    mock_inventory.get_stock.return_value = 2  # Less than required 3

    with pytest.raises(InventoryShortageError, match="Not enough stock for prod-A"):
        order.checkout()

    mock_inventory.get_stock.assert_called_once_with("prod-A")
    # Ensure payment was NOT attempted
    mock_payment.charge.assert_not_called()


def test_checkout_payment_declined(order, mock_inventory, mock_payment):
    order.add_item("prod-A", 50.0, 1)
    mock_inventory.get_stock.return_value = 10
    mock_payment.charge.return_value = False  # Payment declined

    with pytest.raises(PaymentFailedError, match="Transaction declined by gateway"):
        order.checkout()

    mock_inventory.get_stock.assert_called_once_with("prod-A")
    mock_payment.charge.assert_called_once_with(50.0, "USD")
    # Ensure stock was NOT decremented when payment failed
    mock_inventory.decrement_stock.assert_not_called()


def test_checkout_payment_gateway_exception(order, mock_inventory, mock_payment):
    order.add_item("prod-A", 50.0, 1)
    mock_inventory.get_stock.return_value = 10
    mock_payment.charge.side_effect = Exception("Connection timeout")

    with pytest.raises(PaymentFailedError, match="Payment gateway error: Connection timeout"):
        order.checkout()

    mock_inventory.decrement_stock.assert_not_called()


def test_checkout_success(order, mock_inventory, mock_payment):
    # Setup order with multiple items (> $100 subtotal for 10% discount)
    order.add_item("prod-A", 80.0, 1)
    order.add_item("prod-B", 40.0, 1)
    # Total = 120.0, Discounted (10%) = 108.0

    mock_inventory.get_stock.side_effect = lambda product_id: {"prod-A": 5, "prod-B": 10}[product_id]
    mock_payment.charge.return_value = True

    result = order.checkout()

    # Verify return value
    assert result == {"status": "success", "charged_amount": 108.0}
    assert order.is_paid is True
    assert order.status == "COMPLETED"

    # Verify inventory stock checks
    assert mock_inventory.get_stock.call_count == 2
    mock_inventory.get_stock.assert_any_call("prod-A")
    mock_inventory.get_stock.assert_any_call("prod-B")

    # Verify payment charge with exact discounted amount
    mock_payment.charge.assert_called_once_with(108.0, "USD")

    # Verify inventory decrement calls
    assert mock_inventory.decrement_stock.call_count == 2
    mock_inventory.decrement_stock.assert_any_call("prod-A", 1)
    mock_inventory.decrement_stock.assert_any_call("prod-B", 1)

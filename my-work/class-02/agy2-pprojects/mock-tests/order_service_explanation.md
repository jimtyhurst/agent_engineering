Viewed order_service.py:1-123

The [`order_service.py`](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/mock-tests/order_service.py) file implements an e-commerce order checkout flow designed around **Dependency Injection**, making it ideal for unit testing with mocks.

---

### Overview of Components

#### 1. Custom Exceptions
- [`InventoryShortageError`](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/mock-tests/order_service.py#L4-L6): Raised when an item's requested quantity exceeds available stock.
- [`PaymentFailedError`](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/mock-tests/order_service.py#L8-L10): Raised when payment processing fails or is declined.
- [`InvalidOrderError`](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/mock-tests/order_service.py#L12-L14): Raised when an invalid business operation occurs (e.g., checking out an empty cart).

#### 2. External Service Interfaces (Designed to be Mocked)
- [`InventoryService`](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/mock-tests/order_service.py#L17-L25): Declares `get_stock(product_id)` and `decrement_stock(product_id, quantity)`. Base methods raise `NotImplementedError`.
- [`PaymentGateway`](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/mock-tests/order_service.py#L26-L30): Declares `charge(amount, currency)`. Base method raises `NotImplementedError`.

#### 3. Core Business Logic — [`Order`](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/mock-tests/order_service.py#L32-L123) Class

| Method / Property | Responsibilities |
| :--- | :--- |
| [`__init__`](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/mock-tests/order_service.py#L33-L45) | Receives `inventory_service` and `payment_gateway` via dependency injection along with `customer_email` and `is_vip` flag. Initializes cart items dictionary and default status (`DRAFT`). |
| [`add_item`](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/mock-tests/order_service.py#L47-L57) | Validates price ($\ge 0$) and quantity ($> 0$), adding new products or updating quantities of existing items. |
| [`remove_item`](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/mock-tests/order_service.py#L59-L63) | Removes a product completely from the cart. |
| [`total_price`](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/mock-tests/order_service.py#L64-L67) | Property that computes raw subtotal before any discounts. |
| [`apply_discount`](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/mock-tests/order_service.py#L69-L83) | Applies discount tiers:<br>• **VIP customers**: 20% discount (`total * 0.8`) regardless of total.<br>• **Regular customers**: 10% discount (`total * 0.9`) if total exceeds $100.<br>• Otherwise full price. |
| [`checkout`](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/mock-tests/order_service.py#L85-L123) | Orchestrates end-to-end checkout flow:<br>1. Checks that cart is not empty.<br>2. Queries `inventory.get_stock()` for each item.<br>3. Computes final price with [`apply_discount()`](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/mock-tests/order_service.py#L69-L83).<br>4. Calls `payment.charge(final_amount, "USD")`.<br>5. Calls `inventory.decrement_stock()` upon successful payment.<br>6. Marks order `is_paid = True` and `status = "COMPLETED"`. |
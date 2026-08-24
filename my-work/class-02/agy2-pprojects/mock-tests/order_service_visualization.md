Here are visual diagrams illustrating the structure of the [`Order`](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/mock-tests/order_service.py#L32-L123) class, its dependencies, and the step-by-step [`checkout()`](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/mock-tests/order_service.py#L85-L123) sequence.

---

### 1. Class & Dependency Structure

This class diagram highlights the **Dependency Injection** pattern, showing how [`Order`](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/mock-tests/order_service.py#L32-L123) depends on external service interfaces ([`InventoryService`](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/mock-tests/order_service.py#L17-L25) and [`PaymentGateway`](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/mock-tests/order_service.py#L26-L30)) and which exceptions it may raise.

```mermaid
classDiagram
    class Order {
        +InventoryService inventory
        +PaymentGateway payment
        +str customer_email
        +bool is_vip
        +dict items
        +bool is_paid
        +str status
        +add_item(product_id, price, quantity)
        +remove_item(product_id)
        +float total_price
        +apply_discount() float
        +checkout() dict
    }

    class InventoryService {
        <<Interface>>
        +get_stock(product_id) int
        +decrement_stock(product_id, quantity)
    }

    class PaymentGateway {
        <<Interface>>
        +charge(amount, currency) bool
    }

    class InventoryShortageError {
        <<Exception>>
    }
    class PaymentFailedError {
        <<Exception>>
    }
    class InvalidOrderError {
        <<Exception>>
    }

    Order "1" --> "1" InventoryService : injects & calls
    Order "1" --> "1" PaymentGateway : injects & calls
    Order ..> InventoryShortageError : raises on low stock
    Order ..> PaymentFailedError : raises on payment failure
    Order ..> InvalidOrderError : raises on empty cart
```

---

### 2. Checkout Workflow (Sequence Diagram)

This sequence diagram details the precise execution path when [`checkout()`](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/mock-tests/order_service.py#L85-L123) is called:

```mermaid
sequenceDiagram
    autonumber
    actor Caller
    participant Order as Order
    participant Inv as InventoryService
    participant Pay as PaymentGateway

    Caller->>Order: checkout()

    alt 1. Cart is empty
        Order-->>Caller: raise InvalidOrderError
    end

    loop 2. Check stock for each item in cart
        Order->>Inv: get_stock(product_id)
        Inv-->>Order: available_stock
        alt Available stock < requested quantity
            Order-->>Caller: raise InventoryShortageError
        end
    end

    Note over Order: 3. Calculate final amount<br/>(apply_discount)

    Order->>Pay: charge(final_amount, "USD")
    Pay-->>Order: success (bool) or Exception
    alt Charge returns False or throws error
        Order-->>Caller: raise PaymentFailedError
    end

    loop 4. Decrement stock (Only if payment succeeded)
        Order->>Inv: decrement_stock(product_id, quantity)
    end

    Note over Order: 5. State update:<br/>is_paid = True<br/>status = "COMPLETED"

    Order-->>Caller: return {"status": "success", "charged_amount": final_amount}
```

---

### 3. Discount Logic Decision Tree

This flowchart summarizes how [`apply_discount()`](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/mock-tests/order_service.py#L69-L83) calculates the final amount:

```mermaid
flowchart TD
    Start(["Calculate Discount"]) --> IsVIP{"Is customer VIP?"}
    IsVIP -- Yes --> Flat20["Apply 20% off<br/>round(total * 0.8, 2)"]
    IsVIP -- No --> CheckTotal{"Is total > $100?"}
    CheckTotal -- Yes --> Discount10["Apply 10% off<br/>round(total * 0.9, 2)"]
    CheckTotal -- No --> FullPrice["No discount<br/>round(total, 2)"]

    Flat20 --> Output(["Return Final Price"])
    Discount10 --> Output
    FullPrice --> Output
```

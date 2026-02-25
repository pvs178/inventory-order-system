# inventory-order-system

Inventory and orders with hierarchical categories. FastAPI + PostgreSQL.

**Run:** `docker compose up --build`

- API: http://localhost:8000  
- Docs: http://localhost:8000/docs  

**Add item to order:** `POST /orders/{order_id}/items` — body: `{"nomenclature_id": 1, "quantity": 2}`. If the item already exists in the order, quantity is increased. Returns 400 when stock is insufficient.

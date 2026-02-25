from sqlalchemy import select, func
from sqlalchemy.orm import aliased

from app.db.models import Category, Client, Order, OrderItem

CLIENT_ORDER_TOTALS_SQL = """
SELECT c.name AS client_name, COALESCE(SUM(oi.quantity * oi.price), 0) AS total_sum
FROM clients c
LEFT JOIN orders o ON o.client_id = c.id
LEFT JOIN order_items oi ON oi.order_id = o.id
GROUP BY c.id, c.name
"""

CATEGORY_CHILDREN_COUNT_SQL = """
SELECT c.id, c.name, COUNT(ch.id) AS children_count
FROM categories c
LEFT JOIN categories ch ON ch.parent_id = c.id
GROUP BY c.id, c.name
"""

TOP5_PRODUCTS_LAST_MONTH_SQL = """
WITH RECURSIVE category_root AS (
    SELECT id, name, parent_id, id AS root_id, name AS root_name
    FROM categories
    WHERE parent_id IS NULL
    UNION ALL
    SELECT c.id, c.name, c.parent_id, r.root_id, r.root_name
    FROM categories c
    JOIN category_root r ON c.parent_id = r.id
)
SELECT
    n.name AS product_name,
    cr.root_name AS category_level1,
    SUM(oi.quantity)::NUMERIC AS total_quantity
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
JOIN nomenclature n ON n.id = oi.nomenclature_id
LEFT JOIN category_root cr ON cr.id = n.category_id
WHERE o.created_at >= date_trunc('month', current_date - interval '1 month')
  AND o.created_at < date_trunc('month', current_date)
GROUP BY n.id, n.name, cr.root_id, cr.root_name
ORDER BY total_quantity DESC
LIMIT 5
"""

TOP5_PRODUCTS_LAST_MONTH_VIEW_SQL = f"""
CREATE OR REPLACE VIEW view_top5_products_last_month AS
{TOP5_PRODUCTS_LAST_MONTH_SQL.strip()}
"""


def client_order_totals():
    return (
        select(
            Client.name.label("client_name"),
            func.coalesce(func.sum(OrderItem.quantity * OrderItem.price), 0).label(
                "total_sum"
            ),
        )
        .select_from(Client)
        .outerjoin(Order, Order.client_id == Client.id)
        .outerjoin(OrderItem, OrderItem.order_id == Order.id)
        .group_by(Client.id, Client.name)
    )


def category_first_level_children_count():
    child = aliased(Category)
    return (
        select(
            Category.id,
            Category.name,
            func.count(child.id).label("children_count"),
        )
        .outerjoin(child, child.parent_id == Category.id)
        .group_by(Category.id, Category.name)
    )

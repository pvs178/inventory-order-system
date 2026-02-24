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

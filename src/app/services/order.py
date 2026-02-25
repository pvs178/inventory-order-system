from decimal import Decimal

from sqlalchemy.orm import Session

from app.db.models import Nomenclature, Order, OrderItem


class OrderNotFoundError(Exception):
    pass


class NomenclatureNotFoundError(Exception):
    pass


class InsufficientStockError(Exception):
    def __init__(self, available: Decimal, requested: Decimal) -> None:
        self.available = available
        self.requested = requested
        super().__init__(f"Недостаточно товара: в наличии {available}, запрошено {requested}")


def add_item_to_order(
    session: Session,
    order_id: int,
    nomenclature_id: int,
    quantity: Decimal,
) -> OrderItem:
    order = session.get(Order, order_id)
    if order is None:
        raise OrderNotFoundError()

    nomenclature = session.get(Nomenclature, nomenclature_id)
    if nomenclature is None:
        raise NomenclatureNotFoundError()

    existing = next(
        (item for item in order.items if item.nomenclature_id == nomenclature_id),
        None,
    )

    if existing is not None:
        new_total = existing.quantity + quantity
        if nomenclature.quantity < new_total:
            raise InsufficientStockError(nomenclature.quantity, new_total)
        existing.quantity = new_total
        session.flush()
        session.refresh(existing)
        return existing

    if nomenclature.quantity < quantity:
        raise InsufficientStockError(nomenclature.quantity, quantity)

    item = OrderItem(
        order_id=order_id,
        nomenclature_id=nomenclature_id,
        quantity=quantity,
        price=nomenclature.price,
    )
    session.add(item)
    session.flush()
    session.refresh(item)
    return item

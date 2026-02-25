from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.schemas import AddItemToOrderRequest, OrderItemResponse
from app.services.order import (
    InsufficientStockError,
    NomenclatureNotFoundError,
    OrderNotFoundError,
    add_item_to_order,
)

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/{order_id}/items", response_model=OrderItemResponse)
def add_item(
    order_id: int,
    body: AddItemToOrderRequest,
    db: Session = Depends(get_db),
) -> OrderItemResponse:
    try:
        item = add_item_to_order(
            session=db,
            order_id=order_id,
            nomenclature_id=body.nomenclature_id,
            quantity=body.quantity,
        )
        return OrderItemResponse.model_validate(item)
    except OrderNotFoundError:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    except NomenclatureNotFoundError:
        raise HTTPException(status_code=404, detail="Номенклатура не найдена")
    except InsufficientStockError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Недостаточно товара в наличии: {e.available}, запрошено {e.requested}",
        )

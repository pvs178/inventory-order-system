from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class AddItemToOrderRequest(BaseModel):
    nomenclature_id: int = Field(..., gt=0)
    quantity: Decimal = Field(..., gt=0)


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    nomenclature_id: int
    quantity: Decimal
    price: Decimal

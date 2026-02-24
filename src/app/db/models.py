from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    parent: Mapped["Category | None"] = relationship(
        "Category",
        remote_side="Category.id",
        back_populates="children",
        foreign_keys=[parent_id],
    )
    children: Mapped[list["Category"]] = relationship(
        "Category",
        back_populates="parent",
        foreign_keys=[parent_id],
        cascade="all, delete-orphan",
    )
    nomenclatures: Mapped[list["Nomenclature"]] = relationship(
        "Nomenclature",
        back_populates="category",
        foreign_keys="Nomenclature.category_id",
    )

    def __repr__(self) -> str:
        return f"Category(id={self.id}, name={self.name!r}, parent_id={self.parent_id})"


class Nomenclature(Base):
    __tablename__ = "nomenclature"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    quantity: Mapped[Decimal] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        default=Decimal("0"),
    )
    price: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )

    category: Mapped["Category | None"] = relationship(
        "Category",
        back_populates="nomenclatures",
        foreign_keys=[category_id],
    )
    order_items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="nomenclature",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"Nomenclature(id={self.id}, name={self.name!r})"


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    address: Mapped[str] = mapped_column(Text, nullable=False)

    orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="client",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"Client(id={self.id}, name={self.name!r})"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    client: Mapped["Client"] = relationship("Client", back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
        order_by="OrderItem.id",
    )

    def __repr__(self) -> str:
        return f"Order(id={self.id}, client_id={self.client_id})"


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    nomenclature_id: Mapped[int] = mapped_column(
        ForeignKey("nomenclature.id", ondelete="RESTRICT"),
        index=True,
        nullable=False,
    )
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    nomenclature: Mapped["Nomenclature"] = relationship(
        "Nomenclature",
        back_populates="order_items",
    )

    def __repr__(self) -> str:
        return (
            f"OrderItem(id={self.id}, order_id={self.order_id}, "
            f"nomenclature_id={self.nomenclature_id})"
        )

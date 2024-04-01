from datetime import date, datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import db


class Item(db.Model):
    __tablename__ = 'item'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now())
    name: Mapped[str] = mapped_column(String(200))
    amount: Mapped[float]
    bill_id: Mapped[int] = mapped_column(ForeignKey("bill.id"))

    def __repr__(self):
        return f"<{self.__class__.__name__}(name='{self.name}')>"


class Bill(db.Model):
    __tablename__ = 'bill'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now())
    date_of_expense: Mapped[date]
    tax_amount: Mapped[float]
    items: Mapped[list[Item]] = relationship()
    image: Mapped[str] = mapped_column(String(200))  # file location of the bill image
    raw_image: Mapped[str] = mapped_column(String(200))

    def __repr__(self):
        return f"<{self.__class__.__name__}(id='{self.id}')>"


class Tag(db.Model):
    __tablename__ = 'tag'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now())
    name: Mapped[str] = mapped_column(String(50))

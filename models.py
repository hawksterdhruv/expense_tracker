from datetime import date

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db import db


class ExpenseModel(db.Model):
    __tablename__ = 'expenses'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    amount: Mapped[float]
    date_of_expense: Mapped[date]

    # def to_dict(self):
    #     return {
    #         'id': self.id,
    #         'name': self.name,
    #         'amount': self.amount,
    #         'date_of_expense': self.date_of_expense
    #     }
    #
    # @classmethod
    # def from_dict(cls, data):
    #     return cls(**data)

    def __repr__(self):
        # <ExpenseModel(name={self.name}, amount={self.amount}, date_of_expense={self.date_of_expense}>
        return f"<ExpenseModel(name='{self.name}')>"

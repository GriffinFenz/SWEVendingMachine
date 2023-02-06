from dataclasses import dataclass
from typing import List, Optional

from app.extensions import db
from datetime import datetime


@dataclass
class StockRecord(db.Model):
    machine_id: int
    product_id: int
    snapshot_time: datetime
    stock_amount: int

    machine_id = db.Column(
        db.Integer,
        db.ForeignKey("Machines.machine_id", ondelete="CASCADE"),
        primary_key=True,
    )
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("Products.product_id", ondelete="CASCADE"),
        primary_key=True,
    )
    snapshot_time = db.Column(
        db.DateTime, primary_key=True, default=datetime.now(), nullable=False
    )
    stock_amount = db.Column(db.Integer, nullable=False)

    @staticmethod
    def snapshot(machine_id: int, product_id: int):
        from app.models.machine_stock import MachineStock

        machine_stock = db.session.get(
            MachineStock, {"machine_id": int(machine_id), "product_id": int(product_id)}
        )

        if machine_stock:
            stock_record = StockRecord(
                machine_id=machine_id,
                product_id=product_id,
                stock_amount=machine_stock.stock_quantity,
                snapshot_time=datetime.now(),
            )
            db.session.add(stock_record)
            db.session.commit()

    @staticmethod
    def product_time_stamp_in_records(product_id: int) -> Optional[List["StockRecord"]]:
        stock_record = StockRecord.query.filter_by(product_id=product_id).all()
        return stock_record

    @staticmethod
    def machine_time_stamp_in_records(machine_id: int) -> Optional[List["StockRecord"]]:
        stock_record = StockRecord.query.filter_by(machine_id=machine_id).all()
        return stock_record


def take_snapshot(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)

        # Save the snapshot
        StockRecord.snapshot(
            machine_id=kwargs.get("machine_id"), product_id=kwargs.get("product_id")
        )

        return response

    return wrapper

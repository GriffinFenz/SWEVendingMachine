from dataclasses import dataclass

from app.extensions import db
from datetime import date


@dataclass
class StockRecord(db.Model):
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
        db.DateTime, primary_key=True, default=date.today(), nullable=False
    )
    stock_amount = db.Column(db.Integer, nullable=False)

    @staticmethod
    def snapshot(machine_id: int, product_id: int):
        from app.models.machine_stock import MachineStock

        print(machine_id)
        print(product_id)

        machine_stock = db.session.get(
            MachineStock, {"machine_id": int(machine_id), "product_id": int(product_id)}
        )

        if machine_stock:
            stock_record = StockRecord(
                machine_id=machine_id,
                product_id=product_id,
                stock_amount=machine_stock.stock_quantity,
            )
            db.session.add(stock_record)
            db.session.commit()
            print("Debug: Snapshot taken")


def take_snapshot(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)

        # Save the snapshot
        StockRecord.snapshot(
            machine_id=kwargs.get("machine_id"), product_id=kwargs.get("product_id")
        )

        return response

    return wrapper

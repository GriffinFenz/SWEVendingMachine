from app.extensions import db
from dataclasses import dataclass


@dataclass
class MachineStock(db.Model):
    stock_quantity: int

    machine_id = db.Column(db.Integer, db.ForeignKey('Machines.machine_id', ondelete='CASCADE'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.product_id', ondelete='CASCADE'), primary_key=True)
    stock_quantity = db.Column('stock_quantity', db.Integer, nullable=False)

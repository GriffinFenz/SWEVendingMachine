from app.extensions import db
from dataclasses import dataclass


@dataclass
class MachineStock(db.Model):
    stock_quantity: int

    machine_id = db.Column(db.Integer, db.ForeignKey('Machines.machine_id', ondelete='CASCADE'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.product_id', ondelete='CASCADE'), primary_key=True)
    stock_quantity = db.Column('stock_quantity', db.Integer, nullable=False)

    @staticmethod
    def find_by_ids(machine_id, product_id):
        return MachineStock.query.filter(MachineStock.machine_id == {machine_id},
                                         MachineStock.product_id == {product_id}).first()

    @staticmethod
    def add_product_to_machine(machine_id, product_id, amount):
        stock_exists = MachineStock.find_by_ids(machine_id, product_id)
        if stock_exists is None:
            new_stock = MachineStock(machine_id=machine_id, product_id=product_id, stock_quantity=amount)
            db.session.add(new_stock)
            db.session.commit()
            return True
        return False

    @staticmethod
    def edit_stock(product_id, machine_id, amount):
        stock_exists = MachineStock.find_by_ids(machine_id, product_id)
        if stock_exists is not None:
            stock_exists.stock_quantity = amount
            db.session.commit()
            return True
        return False

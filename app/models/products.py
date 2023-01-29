from app.app import db
from dataclasses import dataclass


@dataclass
class Products(db.Model):
    __tablename__ = 'Products'
    product_id: int
    product_name: str
    product_price: float

    product_id = db.Column('product_id', db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column('product_name', db.String(40), unique=True, nullable=False)
    product_price = db.Column('product_price', db.DECIMAL(7, 2), nullable=False)

    machine_products = db.relationship("MachineStock", backref="Products", lazy=True, passive_deletes=True)

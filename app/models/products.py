from app.extensions import db
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

    @staticmethod
    def find_by_id(product_id):
        return Products.query.get(product_id)

    @staticmethod
    def find_by_name(product_name):
        return Products.query.filter(Products.product_name == product_name).first()

    @staticmethod
    def add_product(product_name, product_price):
        product_exists = Products.find_by_name(product_name)
        if product_exists is None:
            new_product = Products(product_name=product_name, product_price=product_price)
            db.session.add(new_product)
            db.session.commit()
            return True
        return False

    @staticmethod
    def remove_product(product_id):
        product_exists = Products.find_by_id(product_id)
        if product_exists is None:
            return False
        Products.query.filter(Products.product_id == product_id).delete()
        db.session.commit()
        return True

    # Returns 1 is the machine to be changed does not exist, Return 2 if new name is a duplicate name,
    # 0 if everything worked
    @staticmethod
    def edit_product(product_id, product_name, product_price):
        product_to_change = Products.find_by_id(product_id)
        if product_to_change is None:
            return 1
        product_duplicate_check = Products.find_by_name(product_name)
        if product_duplicate_check is None:
            product_to_change.product_name = product_name
            product_to_change.product_price = product_price
            db.session.commit()
            return 0
        return 2

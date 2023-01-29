from app import db, app
from dataclasses import dataclass


@dataclass
class Machines(db.Model):
    __tablename__ = 'Machines'
    machine_id: int
    machine_name: str
    machine_location: str

    machine_id = db.Column('machine_id', db.Integer, primary_key=True, autoincrement=True)
    machine_name = db.Column('machine_name', db.String(20), unique=True, nullable=False)
    machine_location = db.Column('machine_location', db.String(150), nullable=False)

    products = db.relationship("MachineStock", backref="Machines", lazy=True, passive_deletes=True)


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


@dataclass
class MachineStock(db.Model):
    stock_quantity: int

    machine_id = db.Column(db.Integer, db.ForeignKey('Machines.machine_id', ondelete='CASCADE'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.product_id', ondelete='CASCADE'), primary_key=True)
    stock_quantity = db.Column('stock_quantity', db.Integer, nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

        machine1 = Machines(machine_name='Bob', machine_location='yes')
        machine2 = Machines(machine_name='BetterBob', machine_location='yes too')

        product1 = Products(product_name='Coke', product_price='20')
        product2 = Products(product_name='Cookies', product_price='100')

        stock1 = MachineStock(machine_id='1', product_id='1', stock_quantity='5')
        stock2 = MachineStock(machine_id='1', product_id='2', stock_quantity='5')

        db.session.add(machine1)
        db.session.add(machine2)
        db.session.add(product1)
        db.session.add(product2)
        db.session.add(stock1)
        db.session.add(stock2)
        db.session.commit()

        Products.query.filter_by(product_id=2).delete()
        db.session.commit()

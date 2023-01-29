from app.app import db, app
from app.models.machines import Machines
from app.models.products import Products
from app.models.machine_stock import MachineStock


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

        # Products.query.filter_by(product_id=2).delete()
        # db.session.commit()
        
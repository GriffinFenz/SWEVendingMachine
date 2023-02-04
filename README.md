[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=GriffinFenz_SWEVendingMachine&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=GriffinFenz_SWEVendingMachine)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=GriffinFenz_SWEVendingMachine&metric=coverage)](https://sonarcloud.io/summary/new_code?id=GriffinFenz_SWEVendingMachine)

# Vending Machine Project
By: Naphong Chadha 6380797

---

### How to run the project:
- Prerequisites:
  - Have a docker running with the credentials in cred.yaml
  - Have a schema called vendingmachine
  - Download everything listen in requirements.txt
- python run.py </br>
This will generate the test database in the app -> models -> test.db file

---

### Project Directory (How to Navigate):
- SWEVendingMachine Directory:
  - app Directory:
    - models Directory:
      - machine_stock.py
      - machines.py
      - products.py
      - testdb.py
    - routes Directory:
      - machines.py
      - products.py
      - stock.py
    - init.py
    - app.py
    - extensions.py
  - cred.yaml
  - README.md
  - requirements.txt
  - run.py (The entrypoint of the program)

---

### How to use the features:


#### Machines:
1. "127.0.0.1:5000/machine?id=1" </br>
    Viewing the contents of one vending machine </br>
    GET Method


2. "127.0.0.1:5000/all-machines" </br>
    View all the vending machines in MUIC </br>
    GET Method


3. "127.0.0.1:5000/machine/create" </br>
    Create a new vending machine </br>
    Json format: { "location": "-", "machine_name": "-" }</br>
    POST Method


4. "127.0.0.1:5000/machine/delete" </br>
    Delete a vending machine that currently exists </br>
    Json format: { "machine_id": "-" }
    POST Method


5. "127.0.0.1:5000/machine/edit" </br>
    Edit the name or location of a machine that currently exists </br>
    Json format: { "machine_id": "-", "machine_name": "-", "location": "-" </br>
    POST Method


#### Products/Items:

1. "127.0.0.1:5000/product?id=1" </br>
    Viewing the contents of one product </br>
    GET Method


2. "127.0.0.1:5000/all-products" </br>
    View all the products available </br>
    GET Method


3. "127.0.0.1:5000/product/create" </br>
    Create a new product </br>
    Json format: { "item_name": "-", "price": - }</br>
    POST Method


4. "127.0.0.1:5000/product/delete" </br>
    Delete a product that currently exists </br>
    Json format: { "item_id": "-" }
    POST Method


5. "127.0.0.1:5000/product/edit" </br>
    Edit the price of a product that currently exists </br>
    Json format: { "item_id": "-", "price": - }</br>
    POST Method


#### Machine Stock:

1. "127.0.0.1:5000/stock/add" </br>
    Add a product to a vending machine of your choice </br>
    Json format: { "machine_id": "-", "item_id": "-", "amount": - } </br>
    POST Method


2. "127.0.0.1:5000/stock/edit" </br>
    Edit the amount of product in a vending machine of your choice that currently exists </br>
    Json format: { "machine_id": "-", "item_id": "-", "amount": - } </br>
    POST Method

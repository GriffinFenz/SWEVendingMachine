# Assuming the database is already setup according to the vendingmachinescript.sql file in scripts directory
from app import read_all_machines


# It just complains at me when I run it so imma not include it

def test_read_all_machines():
    got = [
    {
        "location": "Toilet",
        "machine_id": 2,
        "machine_name": "Cool Machine :D"
    }
        ]
    assert got == read_all_machines()



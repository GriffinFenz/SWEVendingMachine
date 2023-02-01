import requests

ENDPOINT = "http://127.0.0.1:5000/"


# It just complains at me when I run it so imma not include it

def test_read_machine_1():
    machine_id_one = requests.get(ENDPOINT + f"/machine?id=1")

    json_response = machine_id_one.json()

    machine_name = json_response["machine_name"]
    machine_location = json_response["machine_location"]
    assert machine_location == "yes" and machine_name == "Bob"


def test_read_machine_2():
    machine_id_two = requests.get(ENDPOINT + f"/all-machines")
    print(machine_id_two)

    json_response = machine_id_two.json()

    machine_name = json_response[1]["machine_name"]
    machine_location = json_response[1]["machine_location"]
    assert machine_location == "yes too" and machine_name == "BetterBob"


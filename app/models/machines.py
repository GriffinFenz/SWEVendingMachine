from dataclasses import dataclass

from app.extensions import db


@dataclass
class Machines(db.Model):
    __tablename__ = "Machines"
    machine_id: int
    machine_name: str
    machine_location: str

    machine_id = db.Column(
        "machine_id", db.Integer, primary_key=True, autoincrement=True
    )
    machine_name = db.Column("machine_name", db.String(20), unique=True, nullable=False)
    machine_location = db.Column("machine_location", db.String(150), nullable=False)

    products = db.relationship(
        "MachineStock", backref="Machines", lazy=True, passive_deletes=True
    )

    @staticmethod
    def find_by_id(machine_id: int) -> "Machines":
        return db.session.get(Machines, {"machine_id": machine_id})

    @staticmethod
    def find_by_name(machine_name: str) -> "Machines":
        return Machines.query.filter(Machines.machine_name == machine_name).first()

    @staticmethod
    def add_machine(machine_name: str, machine_location: str) -> bool:
        machine_exists = Machines.find_by_name(machine_name)
        if machine_exists is None:
            new_machine = Machines(
                machine_name=machine_name, machine_location=machine_location
            )
            db.session.add(new_machine)
            db.session.commit()
            return True
        return False

    @staticmethod
    def remove_machine(machine_id: int) -> bool:
        machine_exists = Machines.find_by_id(machine_id)
        if machine_exists is None:
            return False
        Machines.query.filter(Machines.machine_id == machine_id).delete()
        db.session.commit()
        return True

    # Returns 1 is the machine to be changed does not exist, Return 2 if new name is a duplicate name,
    # 0 if everything worked
    @staticmethod
    def edit_machine(machine_id: int, machine_name: str, machine_location: str) -> int:
        machine_to_change = Machines.find_by_id(machine_id)
        if machine_to_change is None:
            return 1
        machine_duplicate_check = Machines.find_by_name(machine_name)
        if machine_duplicate_check is None:
            machine_to_change.machine_name = machine_name
            machine_to_change.machine_location = machine_location
            db.session.commit()
            return 0
        return 2

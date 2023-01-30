from app.extensions import db
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

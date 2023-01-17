DROP SCHEMA IF EXISTS VendingMachine;
CREATE SCHEMA VendingMachine;
USE VendingMachine;
DROP TABLE IF EXISTS machines;

create table machines(
    machine_id int auto_increment NOT NULL, #Would be nice if serial ID is primary ley instead
    location varchar(50) NOT NULL,
    primary key (machine_id)
);

DROP TABLE IF EXISTS items;

create table items(
    item_id int auto_increment NOT NULL,
    item_name varchar(30) NOT NULL UNIQUE,
    primary key (item_id)
);

DROP TABLE IF EXISTS machine_products;

create table machine_products(
    machine_id int NOT NULL,
    item_id int NOT NULL,
    quantity int(3),
    constraint fk_machine
                foreign key (machine_id)
                                references machines(machine_id),
    constraint fk_item
                foreign key (item_id)
                             references items(item_id),
    primary key (machine_id, item_id)
);

INSERT INTO machines(location) VALUES ('MUIC BUILDING')

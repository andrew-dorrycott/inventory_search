BEGIN;

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    description TEXT,
    lastsold DATE,
    shelflife TEXT,
    department TEXT,
    price FLOAT,
    unit TEXT,
    xfor INTEGER,
    cost FLOAT
);

COMMIT;
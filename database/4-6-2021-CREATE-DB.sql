CREATE TABLE users (
    id        INTEGER      PRIMARY KEY AUTOINCREMENT,
    username  VARCHAR (32) NOT NULL
                           UNIQUE,
    password  VARCHAR (32) NOT NULL,
    firstname VARCHAR (32) NOT NULL,
    lastname  VARCHAR (32) NOT NULL,
    email     VARCHAR (32) UNIQUE,
    phone     VARCHAR (32)
);

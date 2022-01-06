DROP TABLE IF EXISTS
    currency_exchange,
    financial_instrument,
    users,
    banks,
    codes,
CASCADE;

CREATE TABLE IF NOT EXISTS banks (
    id INTEGER,
    name VARCHAR(30) NOT NULL,
    contact VARCHAR(15) NOT NULL,
    cooperation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (contact),
    UNIQUE (name),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS users (
    id BIGINT,
    name VARCHAR NOT NULL,
    surname VARCHAR NOT NULL,
    sex CHAR(1) NOT NULL ,
    passport_no VARCHAR NOT NULL,
    nationality VARCHAR NOT NULL,
    date_of_birth DATE NOT NULL ,
    phone VARCHAR,
    registration TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (phone),
    UNIQUE (passport_no),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS codes (
    bank_id INTEGER NOT NULL,
    code varchar(5) NOT NULL,
    meaning VARCHAR(200) NOT NULL,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (bank_id, code),
    FOREIGN KEY (bank_id) REFERENCES banks (id)
);

CREATE TABLE IF NOT EXISTS currency_exchange (
    currency VARCHAR(4),
    coeff DOUBLE PRECISION NOT NULL,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (currency)
);

CREATE TABLE IF NOT EXISTS financial_instrument (
    bank_id INTEGER NOT NULL,
    conn_id INTEGER NOT NULL,
    security_id VARCHAR(20), -- only have Bonds and Stocks
    asset_category VARCHAR(30) NOT NULL,
    symbol VARCHAR(30) NOT NULL UNIQUE,
    description VARCHAR(50) NOT NULL,
    multiplier INTEGER,
    type VARCHAR(10) NOT NULL,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    --UNIQUE (bank_id, security_id),
    PRIMARY KEY (bank_id, conn_id),
    FOREIGN KEY (bank_id) REFERENCES banks (id)
);


CREATE TABLE IF NOT EXISTS change_in_dividend_accruals (
    user_id INTEGER NOT NULL,
    bank_id INTEGER NOT NULL,
    sec_id VARCHAR(20) NOT NULL,
    ex_date DATE NOT NULL,
    pay_date DATE NOT NULL,
    quantity VARCHAR NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
    --FOREIGN KEY (bank_id, sec_id) REFERENCES financial_instrument (bank_id, security_id)
);

DROP TABLE IF EXISTS currency_exchange CASCADE;
DROP TABLE IF EXISTS financial_instrument CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS banks CASCADE;
DROP TABLE IF EXISTS codes CASCADE;

CREATE TABLE IF NOT EXISTS banks (
    id BIGINT,
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
    bank_id BIGINT NOT NULL,
    code VARCHAR(5) NOT NULL,
    meaning VARCHAR(200) NOT NULL,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (bank_id, code),
    FOREIGN KEY (bank_id) REFERENCES banks (id)
);

CREATE TABLE IF NOT EXISTS currency_exchange (
    currency VARCHAR,
    coeff DOUBLE PRECISION NOT NULL,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (currency)
);

CREATE TABLE IF NOT EXISTS financial_instrument (
    bank_id BIGINT NOT NULL,
    conn_id BIGINT NOT NULL,
    security_id VARCHAR(20), -- only have Bonds and Stocks
    asset_category VARCHAR(30) NOT NULL,
    symbol VARCHAR(30) NOT NULL UNIQUE,
    description VARCHAR(50) NOT NULL,
    multiplier BIGINT,
    type VARCHAR(10) NOT NULL,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    --UNIQUE (bank_id, security_id),
    PRIMARY KEY (bank_id, conn_id),
    FOREIGN KEY (bank_id) REFERENCES banks (id)
);


CREATE TABLE IF NOT EXISTS change_in_dividend_accruals (
    user_id BIGINT NOT NULL,
    bank_id BIGINT NOT NULL,
    sec_id VARCHAR(20) NOT NULL,
    ex_date DATE NOT NULL,
    pay_date DATE NOT NULL,
    quantity VARCHAR NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
    --FOREIGN KEY (bank_id, sec_id) REFERENCES financial_instrument (bank_id, security_id)
);

DROP TABLE IF EXISTS
    currency_exchange,
    financial_instrument,
    dividends,
    interests,
    change_in_dividend_accruals,
    trades,
    withholding_tax,
    corporate_actions,
    users,
    banks,
    codes,
    open_positions
CASCADE;

CREATE TABLE banks (
    id INTEGER, -- GENERATED ALWAYS AS IDENTITY, or see -SERIAL
    name VARCHAR(30) NOT NULL,
    contact VARCHAR(15) NOT NULL,
    cooperation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (contact),
    UNIQUE (name),
    PRIMARY KEY (id)
);

CREATE TABLE users (
    id INTEGER, -- GENERATED ALWAYS AS IDENTITY,
    name VARCHAR NOT NULL,
    surname VARCHAR NOT NULL,
    sex CHAR(1) NOT NULL ,
    passport_no VARCHAR NOT NULL,
    nationality VARCHAR NOT NULL,
    date_of_birth DATE NOT NULL ,
    phone VARCHAR,
    registration TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (phone),
    UNIQUE (passport_no),
    PRIMARY KEY (id)
);

CREATE TABLE codes (
    bank_id INTEGER NOT NULL,
    code varchar(5) NOT NULL,
    meaning VARCHAR(200) NOT NULL,
    UNIQUE (bank_id, code),
    FOREIGN KEY (bank_id) REFERENCES banks (id)
);

CREATE TABLE currency_exchange (
    currency VARCHAR(4),
    coeff DOUBLE PRECISION NOT NULL,
    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (currency)
);

CREATE TABLE financial_instrument (
    bank_id INTEGER NOT NULL,
    conn_id INTEGER UNIQUE,
    security_id VARCHAR(20), -- only have Bonds and Stocks
    asset_category VARCHAR(30) NOT NULL,
    symbol VARCHAR(30) NOT NULL UNIQUE,
    description VARCHAR(50) NOT NULL,
    multiplier INTEGER,
    type VARCHAR(10) NOT NULL,
    UNIQUE (bank_id, security_id),
    PRIMARY KEY (bank_id, conn_id),
    FOREIGN KEY (bank_id) REFERENCES banks (id)
);

CREATE TABLE dividends (
    user_id INTEGER NOT NULL,
    bank_id INTEGER NOT NULL,
    sec_id VARCHAR(20) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    date DATE NOT NULL,
    description VARCHAR NOT NULL,
    amount DOUBLE PRECISION NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (currency) REFERENCES currency_exchange (currency),
    FOREIGN KEY (bank_id, sec_id) REFERENCES financial_instrument (bank_id, security_id)
 );

CREATE TABLE interests AS TABLE dividends WITH NO DATA;
ALTER TABLE interests ADD FOREIGN KEY (user_id) REFERENCES users (id);
ALTER TABLE interests ADD FOREIGN KEY (currency) REFERENCES currency_exchange (currency);
ALTER TABLE interests ADD FOREIGN KEY (bank_id, sec_id) REFERENCES financial_instrument (bank_id, security_id);

CREATE TABLE withholding_tax (
    LIKE dividends INCLUDING ALL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (currency) REFERENCES currency_exchange (currency),
    FOREIGN KEY (bank_id, sec_id) REFERENCES financial_instrument (bank_id, security_id)
--     INCLUDING DEFAULTS
--     INCLUDING CONSTRAINTS
--     INCLUDING INDEXES
--     INCLUDING STORAGE
--     INCLUDING COMMENTS
);


CREATE TABLE change_in_dividend_accruals (
    user_id INTEGER NOT NULL,
    bank_id INTEGER NOT NULL,
    sec_id VARCHAR(20) NOT NULL,
    ex_date DATE NOT NULL,
    pay_date DATE NOT NULL,
    quantity VARCHAR NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (bank_id, sec_id) REFERENCES financial_instrument (bank_id, security_id)
);

CREATE TABLE corporate_actions (
    bank_id INTEGER NOT NULL,
    description VARCHAR NOT NULL,
    report_date DATE NOT NULL,
    FOREIGN KEY (bank_id) REFERENCES banks (id)
);

CREATE TABLE trades (
    user_id INTEGER NOT NULL,
    conn_id INTEGER, -- there are no Forex in financial instruments.
    bank_id INTEGER NOT NULL,
    symbol VARCHAR(30) NOT NULL, -- for the case of Forex
    currency VARCHAR(3) NOT NULL,
    datetime TIMESTAMP NOT NULL,
    quantity VARCHAR(12) NOT NULL,
    t_price DOUBLE PRECISION NOT NULL,
    comm_fee DOUBLE PRECISION NOT NULL,
    code VARCHAR(5),
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (currency) REFERENCES currency_exchange (currency),
    FOREIGN KEY (bank_id) REFERENCES banks (id),
    FOREIGN KEY (bank_id, conn_id) REFERENCES financial_instrument (bank_id, conn_id)
);

CREATE TABLE open_positions AS TABLE trades WITH NO DATA;
ALTER TABLE open_positions DROP COLUMN code;
ALTER TABLE open_positions ADD FOREIGN KEY (bank_id, conn_id) REFERENCES financial_instrument (bank_id, conn_id);
ALTER TABLE open_positions ADD FOREIGN KEY (user_id) REFERENCES users (id);
ALTER TABLE open_positions ADD FOREIGN KEY (currency) REFERENCES currency_exchange (currency);

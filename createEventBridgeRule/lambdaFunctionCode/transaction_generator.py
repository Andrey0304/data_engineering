from init_logger import log
import psycopg2
import json
import logging
import create_data
import pandas as pd
from io import StringIO


@log('ERROR')
def copy_data_to_database(cursor, data: pd.DataFrame, table_name: str):
    buffer = StringIO()
    data.to_csv(buffer, header=False, index=False)

    buffer.seek(0)
    cursor.copy_from(buffer, table_name, sep=",", columns=data.columns)
    
    buffer.close()
    print(f"The {table_name} data has been successfully copied to the database.")
    

@log('CRITICAL')
def generator(config: dict, N: int):
    
    conn = psycopg2.connect(**config['db_connection'])
    with conn.cursor() as cursor:
        conn.autocommit = True

        sql = 'SELECT id, registration FROM users;'
        users = pd.io.sql.read_sql_query(sql,  conn)
        users_id = users['id'].values.tolist()
        
        cursor.execute('SELECT code FROM codes;')
        codes = tuple(map(lambda x: x[0], cursor.fetchall()))

        sql = "SELECT * FROM financial_instrument;"
        fin_instrument = pd.io.sql.read_sql_query(sql, conn)
        
        dividends = create_data.create_dividends(users_id, fin_instrument, N)
        interests = create_data.create_interests(dividends.copy(),
                                                fin_instrument,
                                                users_id,
                                                N)
        withholding_tax = create_data.create_withholding_tax(dividends.copy())
        change_in_dividend_accruals = create_data.create_change_in_dividend_accruals(dividends.copy())
        trades = create_data.create_trades(fin_instrument,
                                           users_id,
                                           users,
                                           codes,
                                           N)
        table_names = (
                'dividends',
                'interests',
                'withholding_tax',
                'change_in_dividend_accruals',
                'trades',
            )
        for name in table_names:
            data = locals()[name]
            copy_data_to_database(cursor=cursor, data=data, table_name=name)
    conn.close()
    print('Database connection closed.')

if __name__ == '__main__':
    config = json.load(open('config.json'))
    
    logging.basicConfig(**config['logger'])
    generator(config, N=5)
from init_logger import log
from main import create_rds_instance, connect_to_db, copy_data_to_database 


@log('ERROR')
def generator(N: int):

    endpoint = create_rds_instance(config['instance_params'])
    conn = connect_to_db(config['instance_params'], endpoint)
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
                # 'users',
                # 'banks',
                # 'codes',
                # 'currency_exchange',
                # 'financial_instrument',
                'dividends',
                'interests',
                'withholding_tax',
                'change_in_dividend_accruals',
                'trades',
                # 'open_positions',
                # 'corporate_actions'
            )
        for name in table_names:
            data = locals()[name]
            copy_data_to_database(cursor=cursor, data=data, table_name=name)
    conn.close()
    print('Database connection closed.')

if __name__ == '__main__':
    import os
    import yaml
    import logging
    import create_data
    import pandas as pd

    os.environ['AWS_CONFIG_FILE'] = os.path.join('config', 'aws_config')
    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = os.path.join('config','aws_credentials')

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join('config', 'config.yaml')
    config = yaml.safe_load(open(config_path))

    logging.basicConfig(**config['logger'])
    generator(N=5)
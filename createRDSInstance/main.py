import create_data
from init_logger import log
import pandas as pd
from io import StringIO
import psycopg2
import logging
import time
import boto3
import yaml
import os
from os.path import abspath, dirname
import warnings

warnings.filterwarnings("ignore")


@log('ERROR')
def check_instance_endpoint(client, identifier: str)->str or None:
    
    print("The Instanse is not yet available. Please wait. ^_^ \n")
    start = time.time()
    waiting_time = 0
    while True:
        instance_description = client.describe_db_instances(
                DBInstanceIdentifier=identifier
            )['DBInstances'][0]
        status = instance_description['DBInstanceStatus']
        if status == 'available':
            endpoint = instance_description['Endpoint']['Address']
            break
        elif status != 'stopped':
            if waiting_time == 9:
                print(f'The Instance is not avaliable yet. Status-|{status}|.')
                waiting_time = 0
            time.sleep(3)
            waiting_time += 3
        else:
            response =  input('Would You like to start Instance. Please type yes|no -  ')   
            while True:
                if response == 'yes':
                    client.start_db_instance(DBInstanceIdentifier=identifier)
                    time.sleep(2)
                    break
                elif response == 'no':
                    return None
                while response not in ('yes', 'no'):
                    response = input('Incorrect answer. Please type yes|no - ')
                
    print('\nRDSInstance is available. Waiting time - '
              f'{round(time.time() - start)} second\n')
    return endpoint


@log('CRITICAL')
def create_rds_instance(instance_params: dict)->str or None:
    # [default] configurations are specified in aws_config_files
    session = boto3.Session(profile_name='default')
    client = session.client('rds')

    rds_instances = (instance['DBInstanceIdentifier']
                     for instance in
                     client.describe_db_instances()['DBInstances'])
    identifier = instance_params['DBInstanceIdentifier']

    if identifier in rds_instances:
        print(f"'{identifier}' Instance exists.")

        instance_description = client.describe_db_instances(DBInstanceIdentifier=identifier)['DBInstances'][0]
        status = instance_description['DBInstanceStatus']
        if status == 'available':
            endpoint = instance_description['Endpoint']['Address']
            return endpoint
        if status == 'stoped':
            client.start_db_instance(DBInstanceIdentifier=identifier)
        return check_instance_endpoint(client, identifier)
    
    client.create_db_instance(**instance_params)
    print('The RDSInstance is creating!')

    return check_instance_endpoint(client, identifier)


@log('CRITICAL')
def connect_to_db(instance_params: dict, endpoint: str):
    """ Connect to the PostgreSQL database server """

    conn = None
    
    conn = psycopg2.connect(
            host=endpoint,
            port=instance_params['Port'],
            database=instance_params['DBName'],
            user=instance_params['MasterUsername'],
            password=instance_params['MasterUserPassword']
        )
    print("A connection to the PostgreSQl database has been established. ^_^")

    return conn


@log('ERROR')
def copy_data_to_database(cursor, data: pd.DataFrame, table_name: str):
    # The StringIO module is an in-memory file-like object.
    # When the StringIO object is created it is initialized by passing a string to the constructor.
    buffer = StringIO()

    # Save dataframe to an in memory buffer
    data.to_csv(buffer, header=False, index=False)

    # print(f'Cursor position is index={buffer.tell()}')
    # Set the cursor position on index=0 in the file.
    buffer.seek(0)
    cursor.copy_from(buffer, table_name, sep=",", columns=data.columns)
    
    # print("Is the file closed?", buffer.closed)
    buffer.close()
    print(f"The {table_name} data has been successfully copied to the database.")


@log("CRITICAL")
def main():
    os.chdir(dirname(dirname(abspath(__file__))))
    config_path = os.path.join('config', 'config.yaml')
    config = yaml.safe_load(open(config_path))

    os.environ['AWS_CONFIG_FILE'] = os.path.join('config', 'aws_config')
    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = os.path.join('config','aws_credentials')

    # logging.config.dictConfig(config['logging'])
    logging.basicConfig(**config['logger'])
    
    endpoint = create_rds_instance(config['instance_params'])
    conn = connect_to_db(config['instance_params'], endpoint)
    with conn.cursor() as cursor:
        conn.autocommit = True
        
        # Create database structure
        cursor.execute(open(config['rds_db_structure'], "r").read())
        print('Database structure was successfuly created.')

        # Execute triggers
        cursor.execute(open(config['rds_db_triggers'], "r").read())
        print('Triggers was successfuly execute.')
        
        users = create_data.create_users(200)
        copy_data_to_database(cursor=cursor, data=users, table_name='users')
        
        sql = 'SELECT id, registration FROM users;'
        users = pd.io.sql.read_sql_query(sql,  conn)
        users_id = users['id'].values.tolist()
            
        banks = create_data.create_banks()
        copy_data_to_database(cursor=cursor, data=banks, table_name='banks')
        # banks_id = banks['id'].values.tolist()
        cursor.execute('SELECT id FROM banks;')
        banks_id = tuple(map(lambda x: x[0], cursor.fetchall()))

        codes = create_data.create_codes(banks_id)
        currency_exchange = create_data.create_currency_exchange()
        financial_instrument = create_data.create_financial_instrument(banks_id)
        dividends = create_data.create_dividends(users_id, financial_instrument, 50)
        interests = create_data.create_interests(dividends.copy(),
                                                 financial_instrument,
                                                 users_id,
                                                 50)
        withholding_tax = create_data.create_withholding_tax(dividends.copy())
        change_in_dividend_accruals = create_data.create_change_in_dividend_accruals(
                                                                dividends.copy())
        trades = create_data.create_trades(financial_instrument,
                                            users_id,
                                            users,
                                            codes.code.values,
                                            200)
        open_positions = create_data.create_open_positions(trades.copy())
        corporate_actions = create_data.create_corporate_actions(banks_id)

        table_names = (
            'codes',
            'currency_exchange',
            'financial_instrument',
            'dividends',
            'interests',
            'withholding_tax',
            'change_in_dividend_accruals',
            'trades',
            'open_positions',
            'corporate_actions'
        )
        for name in table_names:
            data = locals()[name]
            copy_data_to_database(cursor=cursor, data=data, table_name=name)
    conn.close()
    print('Database connection closed.')


if __name__ == '__main__':
    main()

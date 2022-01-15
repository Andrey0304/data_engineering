import boto3
import os
import io
from os.path import basename, abspath, dirname
import psycopg2
import pandas as pd
import yaml
from datetime import datetime, timedelta


os.chdir(dirname(abspath(__file__)))

os.environ['AWS_CONFIG_FILE'] = os.path.join('config', 'aws_config')
os.environ['AWS_SHARED_CREDENTIALS_FILE'] = os.path.join('config','aws_credentials')

config_path = os.path.join('config', 'config.yaml')
config = yaml.safe_load(open(config_path))

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
metadata_table = dynamodb.Table('update_metadata')

metadata = {
        d['table']: d['update_time']
        for d in metadata_table.scan()['Items']
    }

datetime_now = datetime.now()

ObjectName = str(datetime_now).replace(' ', '_')
BucketName = 'data-lake-for-me'


def put_object_to_S3(
    conn,
    client,
    tables: tuple,
    metadata: dict,
    metadata_table,
    column_for_check: str
):
    for table in tables:
        datetime_last_update = datetime.strptime(metadata[table], '%Y-%m-%d %H:%M:%S.%f')
        sql = f"""
                SELECT * FROM {table}
                WHERE {column_for_check} >= '{datetime_last_update}' AND
                      {column_for_check} < '{datetime_now}';
               """
        frame = pd.io.sql.read_sql_query(sql,  conn)
        frame.to_parquet(
            f's3://{BucketName}/{table}/{ObjectName}',
            compression='brotli',
            engine='pyarrow',
            index=False
            )
        metadata_table.update_item(
            Key={
                'table': table,
            },
            UpdateExpression='set update_time=:v',
            ExpressionAttributeValues={
                ':v': str(datetime_now),
            },
        )


conn = psycopg2.connect(
        host='database-1.cyiiggb1luvo.eu-central-1.rds.amazonaws.com',
        user='postgres',
        password='postgres',
        dbname='newdb',
        )
transaction_tables = (
                    'dividends',
                    'interests',
                    'withholding_tax',
                    'change_in_dividend_accruals',
                    'trades',
                    'corporate_actions',
                    'open_positions',
                )
static_tables =  (
                'users',
                'banks',
                'codes',
                'currency_exchange',
                'financial_instrument',
                )
put_object_to_S3(
    conn,
    s3_client,
    transaction_tables,
    metadata,
    metadata_table,
    'pay_date'
)
put_object_to_S3(
    conn,
    s3_client,
    static_tables,
    metadata,
    metadata_table,
    'update_time'
)


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

DATETIME = str(datetime.now()).replace(' ', '_')
BucketName = 'data-lake-for-me'

conn = psycopg2.connect(**config['rds'])
s3_client = boto3.client('s3')

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

def put_object_to_S3(
	conn,
	client,
	tables: tuple,
	column_for_check: str
):
	for table in tables:
		sql = f"""
				SELECT * FROM {table}
				WHERE {column_for_check} >= '{datetime.now() - timedelta(hours=100000)}';
			   """
		frame = pd.io.sql.read_sql_query(sql,  conn)
		frame.to_parquet(
			f's3://{BucketName}/{table}/{DATETIME}',
			compression='brotli',
			engine='pyarrow',
			index=False
			)
	
put_object_to_S3(conn, s3_client, transaction_tables, 'pay_date')
put_object_to_S3(conn, s3_client, static_tables, 'update_time')

# buffer = io.BytesIO()
# s3_client.download_fileobj(BucketName, f'trades/{DATETIME}', buffer)
# print(pd.read_parquet(buffer))
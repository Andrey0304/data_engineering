import boto3
import psycopg2
import pytz
import pandas as pd
from datetime import datetime, timedelta

# ObjectName = str(datetime.now(pytz.timezone('Asia/Tbilisi'))).replace(' ', '_')
datetime_str = f'{datetime.now().date()} 23:00:00'
datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

ObjectName = datetime_str.replace(' ', '_')
BucketName = 'data-lake-for-me'

def put_object_to_S3(
	conn,
	client,
	tables: tuple,
	column_for_check: str
):
	for table in tables:
		sql = f"""
				SELECT * FROM {table}
				WHERE {column_for_check} >= '{datetime_obj - timedelta(hours=24)}';
			   """
		frame = pd.io.sql.read_sql_query(sql,  conn)
		frame.to_parquet(
			f's3://{BucketName}/{table}/{ObjectName}',
			compression='brotli',
			engine='pyarrow',
			index=False
			)
	
def lambda_handler(event, context):
    conn = psycopg2.connect(
        host='database-1.cyiiggb1luvo.eu-central-1.rds.amazonaws.com',
        user='postgres',
        password='postgres',
        dbname='newdb',
        )
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
    put_object_to_S3(conn, s3_client, transaction_tables, 'pay_date')
    put_object_to_S3(conn, s3_client, static_tables, 'update_time')
    
    # print(pd.read_parquet('s3://data-lake-for-me/currency_exchange/2022-01-08_23:00:00'))
    print(datetime_obj - timedelta(hours=24))
    return 0

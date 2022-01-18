import boto3
import os
from os.path import basename, abspath, dirname
import psycopg2
import yaml
from datetime import datetime, timedelta


os.chdir(dirname(dirname(abspath(__file__))))
os.environ['AWS_CONFIG_FILE'] = os.path.join('config', 'aws_config')
os.environ['AWS_SHARED_CREDENTIALS_FILE'] = os.path.join('config','aws_credentials')

config_path = os.path.join('config', 'config.yaml')
config = yaml.safe_load(open(config_path))

dynamodb = boto3.resource('dynamodb')
metadata_table = dynamodb.Table('redshift_update_time')

metadata = {
        d['table']: d['update_time']
        for d in metadata_table.scan()['Items']
    }

datetime_now = datetime.now()

ObjectName = str(datetime_now).replace(' ', '_')
BucketName = 'data-lake-for-me'

conn = psycopg2.connect(**config['redshift'])
with conn.cursor() as cursor:
    conn.autocommit = True
       
    # Create database structure
    cursor.execute(open(config['redshift_db_structure'], "r").read())
    print('Redshift Database structure was successfuly created.')

    static_tables =  (
    			'users',
    			'banks',
    			'codes',
                'currency_exchange',
                'financial_instrument',
                )

    for table in static_tables:
    	cursor.execute(
			f"""
			COPY {table}
			FROM 's3://{BucketName}/{table}/{ObjectName}'
			IAM_ROLE 'arn:aws:iam::706509704930:role/service-role/AmazonRedshift-CommandsAccessRole-20220106T170424'
			FORMAT AS PARQUET;
			"""
			)
    	print(f'{table} successfuly upload to Data WareHouse')

    	metadata_table.update_item(
            Key={
                'table': table,
            },
            UpdateExpression='set update_time=:v',
            ExpressionAttributeValues={
                ':v': str(datetime_now),
            },
        )

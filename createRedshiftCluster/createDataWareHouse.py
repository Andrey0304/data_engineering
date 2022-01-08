import boto3
import os
import io
from os.path import basename, abspath, dirname
import psycopg2
import pandas as pd
import yaml
import pytz
from datetime import datetime, timedelta


os.chdir(dirname(dirname(abspath(__file__))))
os.environ['AWS_CONFIG_FILE'] = os.path.join('config', 'aws_config')
os.environ['AWS_SHARED_CREDENTIALS_FILE'] = os.path.join('config','aws_credentials')

config_path = os.path.join('config', 'config.yaml')
config = yaml.safe_load(open(config_path))

ObjectName = f'{datetime.now().date()}_23:00:00'
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


   # def put_object_to_Readshift(
# 	conn,
# 	client,
# 	tables: tuple,
# 	column_for_check: str
# ):
	
# 		sql = f"""
# 				SELECT * FROM {table}
# 			   """
# 		data = pd.io.sql.read_sql_query(sql,  conn)
# 		buffer = StringIO()
# 	    data.to_csv(buffer, header=False, index=False)

# 	    buffer.seek(0)
# 	    cursor.copy_from(buffer, table_name, sep=",", columns=data.columns)
	    
# 	    buffer.close()


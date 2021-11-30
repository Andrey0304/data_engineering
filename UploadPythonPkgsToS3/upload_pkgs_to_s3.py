import os
from os.path import abspath, dirname, basename
import boto3
import yaml

os.chdir(dirname(dirname(abspath(__file__))))

os.environ['AWS_CONFIG_FILE'] = os.path.join('config', 'aws_config')
os.environ['AWS_SHARED_CREDENTIALS_FILE'] = os.path.join('config','aws_credentials')

config_path = os.path.join('config', 'config.yaml')
config = yaml.safe_load(open(config_path))

BucketName = config['BucketName']
Pkgs_Zip_file = config['Pkgs_Zip_file']
Region = config['region']
Key = basename(Pkgs_Zip_file)

s3_client = boto3.client('s3')
list_buckets = s3_client.list_buckets()['Buckets']
list_bucket_names = [bucket['Name'] for bucket in list_buckets]

if BucketName not in list_bucket_names:
    s3_client.create_bucket(
        Bucket=BucketName,
        CreateBucketConfiguration={'LocationConstraint': Region}
    )
else:
    bucket_contents = s3_client.list_objects(Bucket='for-python-pkgs')['Contents']
    keys = [content['Key'] for content in bucket_contents]
    if Key in keys:
        s3_client.delete_object(Bucket=BucketName, Key=Key)

with open(Pkgs_Zip_file, 'wb') as data:
    s3.download_fileobj(BucketName, Key, data)
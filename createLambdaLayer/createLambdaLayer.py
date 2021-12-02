import subprocess
import boto3
import os
from os.path import basename, abspath, dirname
import sys
import yaml
import logging


def install_requirements(
    path_to_dir: str,
    path_to_reqs: str,
    ):
    """Installs the required packages to the given directory"""
    
    if not os.path.exists(path_to_reqs):
        response = subprocess.run(
                        f'pip freeze > {path_to_reqs}',
                        stderr=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        shell=True
                    )
        if response.returncode != 0:
            logging.critical(f'\n{response.stderr}')
            os.remove(path_to_reqs)
            sys.exit()
    if not os.path.exists(path_to_dir):
        os.makedir(path_to_dir)
    
        commands = f"""
                    pip install -r {path_to_reqs} -t {path_to_dir}
                    zip -r python.zip {path_to_dir}
                    """
        response = subprocess.run(
                    commands,
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    shell=True
            )
        if response.returncode != 0:
            logging.critical(f'\n{response.stderr}')
        else:
            print('All dependencies were installed successfully.')


def upload_object_to_s3(
    BucketName: str,
    ObjectName: str,
    Pkgs_Zip_file: str,
    Region: str,
    ):
    
    s3_client = boto3.client('s3')

    list_buckets = s3_client.list_buckets()['Buckets']
    list_bucket_names = [bucket['Name'] for bucket in list_buckets]
    
    if BucketName not in list_bucket_names:
        s3_client.create_bucket(
            Bucket=BucketName,
            CreateBucketConfiguration={'LocationConstraint': Region}
        )
    else:
        S3objects = s3_client.list_objects(Bucket=BucketName)
        if 'Contents' in S3objects:
            keys = [content['Key'] for content in S3objects['Contents']]
            if ObjectName in keys:
                s3_client.delete_object(Bucket=BucketName, Key=ObjectName)

    s3_client.upload_file(Pkgs_Zip_file, BucketName, ObjectName)


def create_lambda_layer(
    LayerName: str,
    BucketName: str,
    ObjectName: str,
    ):

    lambda_client = boto3.client('lambda')
    response = lambda_client.publish_layer_version(
            LayerName=LayerName,
            Description='yaml, pandas, numpy, psycopg2, psycopg2-binary',
            Content={
                'S3Bucket': BucketName,
                'S3Key': ObjectName,
                # 'S3ObjectVersion': '1',
                # 'ZipFile': b'bytes'
            },
            CompatibleRuntimes=['python3.8'],
            CompatibleArchitectures=['x86_64'],
        )


def main():
    os.chdir(dirname(dirname(abspath(__file__))))

    os.environ['AWS_CONFIG_FILE'] = os.path.join('config', 'aws_config')
    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = os.path.join('config','aws_credentials')

    config_path = os.path.join('config', 'config.yaml')
    config = yaml.safe_load(open(config_path))

    PathToDir = config['required_packages_dir']
    PathToReqs = config['required_packages_file']
    BucketName = config['BucketName']
    Pkgs_Zip_file = config['Pkgs_Zip_file']
    Region = config['region']
    LayerName = config['lambdaLayerName']

    ObjectName = basename(Pkgs_Zip_file)
    
    logging.basicConfig(**config['logger'])

    install_requirements(PathToDir, PathToReqs)
    upload_to_s3(BucketName, ObjectName, Pkgs_Zip_file, Region)
    create_lambda_layer(LayerName, BucketName, ObjectName)


if __name__ == '__main__':
    maun()

import yaml
import json
import os
from os.path import basename, abspath, dirname
import boto3


def create_role_for_lambda(RoleName: str, PolicyArn_list: list):

  iam_client = boto3.client('iam')
      
  assume_role_policy_document = json.dumps({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  })

  # Create IAM Role and attach policy 
  iam_client.create_role(
          RoleName = RoleName,
          AssumeRolePolicyDocument = assume_role_policy_document
      )
  role = boto3.resource('iam').Role(RoleName)
  for PolicyArn in PolicyArn_list:
    role.attach_policy(PolicyArn=PolicyArn)


def create_lambda_functon(
    lambdaFunctionName: str,
    lambdaHandler: str,
    lambdaLayerName: str,
    RoleName: str,
    lambdaFunctionCode: str,
    ):

    lambda_client = boto3.client('lambda')

    response = lambda_client.list_layer_versions(LayerName=lambdaLayerName)
    lambdaLayerArn = response['LayerVersions'][0]['LayerVersionArn']

    RoleARN = boto3.resource('iam').Role(RoleName).arn

    lambda_funcions = lambda_client.list_functions()['Functions']
    all_function_names = [function['FunctionName'] for function in lambda_funcions]
    if lambdaFunctionName in all_function_names:
        lambda_client.delete_function(FunctionName=lambdaFunctionName)

    response = lambda_client.create_function(
        FunctionName=lambdaFunctionName,
        Runtime='python3.8',
        Role=RoleARN,
        Handler=lambdaHandler,
        Publish=True,
        PackageType='Zip',
        Architectures=[
            'x86_64',
        ],
        Code={
            'ZipFile': open(lambdaFunctionCode, 'rb').read(),
            # 'S3Bucket': 'string',
            # 'S3Key': 'string',
            # 'S3ObjectVersion': 'string',
        },
        Layers=[
            lambdaLayerArn,
            ],
        Timeout=900 #seconds
)


def create_EventBridge_role(lambdaFunctionName: str, event_config: dict):

    lambda_client = boto3.client('lambda')
    lambdaFunctionArn = lambda_client.get_function_configuration(
        FunctionName=lambdaFunctionName
        )['FunctionArn']

    event_client = boto3.client('events')
    event_client.put_rule(**event_config)
    event_client.put_targets(
        Rule=event_config['Name'],
        Targets=[
            {
                'Id': 'rurLambdaFunction',
                'Arn': lambdaFunctionArn,
            }
        ]
    )


def main():
    os.chdir(dirname(dirname(abspath(__file__))))

    os.environ['AWS_CONFIG_FILE'] = os.path.join('config', 'aws_config')
    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = os.path.join('config','aws_credentials')

    config_path = os.path.join('config', 'config.yaml')
    config = yaml.safe_load(open(config_path))

    RoleName = config["IAMRole"]['RoleName']
    PolicyArn_list = config['IAMRole']['PolicyArn']

    lambda_config = config['lambda']
    lambdaLayerName = lambda_config ['LayerName']
    lambdaFunctionCode = lambda_config['FunctionCode'] # ZipFile
    lambdaFunctionName = lambda_config ['FunctionName']
    lambdaHandler = lambda_config ['Handler']
    
    # create_role_for_lambda(RoleName, PolicyArn_list)
    create_lambda_functon(
        lambdaFunctionName,
        lambdaHandler,
        lambdaLayerName,
        RoleName,
        lambdaFunctionCode,
        )
    # create_EventBridge_role(lambdaFunctionName, config['event'])


if __name__ == '__main__':
    main()
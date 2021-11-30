import boto3
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.environ['AWS_CONFIG_FILE'] = os.path.join('config', 'aws_config')
os.environ['AWS_SHARED_CREDENTIALS_FILE'] = os.path.join('config','aws_credentials')

lambda_client = boto3.client('lambda')

RoleName = 'VPC_RDS_FullAccess'
RoleARN = boto3.resource('iam').Role(RoleName).arn
ZipFile = open('lambdaFunction.zip', 'rb').read()
FunctionName = 'TransactionGenerator'

lambda_funcions = lambda_client.list_functions()['Functions']

all_function_names = [function['FunctionName'] for function in lambda_funcions]
if FunctionName in all_function_names:
	lambda_client.delete_function(FunctionName=FunctionName)

response = lambda_client.create_function(
    FunctionName=FunctionName,
    Runtime='python3.8',
    Role=RoleARN,
    Handler='lambda_function.lambda_hendler',
    Publish=True,
    PackageType='Zip',
    Architectures=['x86_64'],
    Code={
        'ZipFile': ZipFile,
        # 'S3Bucket': 'string',
        # 'S3Key': 'string',
        # 'S3ObjectVersion': 'string',
    },
    Layers=[
    'arn:aws:lambda:eu-central-1:706509704930:layer:sadasdd:1',
       ],
)
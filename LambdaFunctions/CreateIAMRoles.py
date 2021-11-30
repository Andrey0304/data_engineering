import json
import os
import boto3

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.environ['AWS_CONFIG_FILE'] = os.path.join('config', 'aws_config')
os.environ['AWS_SHARED_CREDENTIALS_FILE'] = os.path.join('config','aws_credentials')

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

ROLE_1 = "EventBridgeFullAccess"
ROLE_2 = "VPC_RDS_FullAccess"

# Create EventBridgeFullAccess role and attach policy 
iam_client.create_role(
        RoleName = ROLE_1,
        AssumeRolePolicyDocument = assume_role_policy_document
    )
iam_client.attach_role_policy(
         RoleName=ROLE_1,
         PolicyArn="arn:aws:iam::aws:policy/AmazonEventBridgeFullAccess"
    )

# Create VPC_RDS_FullAccess role and attach policy 
iam_client.create_role(
        RoleName = ROLE_2,
        AssumeRolePolicyDocument = assume_role_policy_document
    )
role_2 = boto3.resource('iam').Role(ROLE_2)
role_2.attach_policy(
         PolicyArn="arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
    )
role_2.attach_policy(
         PolicyArn="arn:aws:iam::aws:policy/AmazonRDSFullAccess"
    )


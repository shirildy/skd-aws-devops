#Author : SHiril K Dubey , updated
#Date : 2023-10-30
#description : This script is used to create a subnet in AWS using Boto3
#VPC : Virtual Private Cloud


import boto3
import logging
from datetime import datetime
from load_config import load_config



# Set environment
env = 'default'
cfg = load_config(env)  

# Set up logging
log_filename = f'logs/create_subnet_{env}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
logging.basicConfig(
    filename=log_filename,
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)   

#List all VPCs in the region
session = boto3.Session(profile_name=cfg.PROFILE_NAME)
ec2_client = session.client('ec2', region_name=cfg.REGION_NAME)

try:
    response = ec2_client.describe_vpcs()
    vpcs = response['Vpcs']
    if not vpcs:
        logging.info("No VPCs found.")
    for vpc in vpcs:
        logging.info(f"Found VPC: {vpc['VpcId']}")
except Exception as e:
    logging.error(f"Error listing VPCs: {str(e)}")  



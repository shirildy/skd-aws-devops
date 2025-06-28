import logging
import boto3
from datetime import datetime
from utils.config_loader import ConfigLoader
from utils.udf import create_volume_from_subnet, attach_volume_to_instance

env = 'dev'
cfg = ConfigLoader(env)

ec2_config = cfg.get('ec2')
if ec2_config is None:
    raise ValueError(f"'ec2' section not found in configuration.")
else:
    print(f"Launching in region: {ec2_config['REGION_NAME']}")
    print(f"in vpc: {ec2_config['VPC_ID']}")
    print(f"in subnet: {ec2_config['SUBNET_ID']}")
    print(f"with security group: {ec2_config['SECURITY_GROUP_ID']}")
    print(f"using key pair: {ec2_config['KEY_PAIR_NAME']}")

#Set up logging

log_filename = f'logs/launch_instance_{env}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
logging.basicConfig(
    filename=log_filename,
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# # Create a session using the default profile
session = boto3.Session(profile_name=ec2_config['PROFILE_NAME'])
ec2_client = session.client('ec2', region_name=ec2_config['REGION_NAME'])



# #create a new EC2 instance 
try:
    response = ec2_client.run_instances(
        ImageId=ec2_config['AMI_ID'],
        InstanceType=ec2_config['INSTANCE_TYPE'],
        MinCount=1,
        MaxCount=1,
        KeyName=ec2_config['KEY_PAIR_NAME'],
        SecurityGroupIds=[ec2_config['SECURITY_GROUP_ID']],
        SubnetId=ec2_config['SUBNET_ID'],
        TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name','Value': 'from boto3 script'}]
        }]
    )
    instance_id = response['Instances'][0]['InstanceId']
    success_msg = f"Launched instance '{instance_id}' in {env} environment."
    print(success_msg)
    logging.info(success_msg)
except Exception as e:
    error_msg = f"Failed to launch EC2 instance: {str(e)}"
    print(error_msg)
    logging.error(error_msg)
    exit(1)



# Wait for instance to be running
try:
    waiter = ec2_client.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance_id])
    print(f"Instance {instance_id} is now running.")
    logging.info(f"Instance {instance_id} is now running.")
except Exception as e:
    error_msg = f"Failed to wait for instance to be running: {str(e)}"
    print(error_msg)
    logging.error(error_msg)    





# Add volume to the instance
try:
    # Create a new volume from the subnet
    subnet_id = ec2_config['SUBNET_ID']
    volume_response = create_volume_from_subnet(
        ec2_client,
        subnet_id,
        size_gib=10,
        tag_key='from-boto3-script',
        tag_value='skd-dev-volume'
    )
    
    volume_id = volume_response['VolumeId']
    print(f"Created volume '{volume_id}' in {env} environment.")
    logging.info(f"Created volume '{volume_id}' in {env} environment.")    

    # Attach the volume to the instance
    attach_response = attach_volume_to_instance(
        ec2_client,
        volume_id,
        instance_id
    )
    
    print(f"Attached volume '{volume_id}' to instance '{instance_id}'.")
    logging.info(f"Attached volume '{volume_id}' to instance '{instance_id}'.")
except Exception as e:
    volume_error_msg = f"Failed to create or attach volume: {str(e)}"
    print(volume_error_msg)
    logging.error(volume_error_msg)


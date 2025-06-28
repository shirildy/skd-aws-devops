import logging
import boto3
from datetime import datetime
from utils.config_loader import ConfigLoader

env = 'dev'
cfg = ConfigLoader(env)

ec2_config = cfg.get('ec2')
if ec2_config is None:
    raise ValueError("❌ 'ec2' section not found in configuration.")
else:
     print(f"Launching in region: {ec2_config['REGION_NAME']}")
    # print(f"in vpc: {ec2_config['VPC_ID']}")
    # print(f"in subnet: {ec2_config['SUBNET_ID']}")
    # print(f"with security group: {ec2_config['SECURITY_GROUP_ID']}")
    # print(f"using key pair: {ec2_config['KEY_PAIR_NAME']}")

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

    # Add volume to the instance
    try:
        # Get subnet's AZ
        subnet_id = ec2_config['SUBNET_ID']
        subnet_info = ec2_client.describe_subnets(SubnetIds=[subnet_id])
        az = subnet_info['Subnets'][0]['AvailabilityZone']
        print(f"Availability Zone: {az}")
        
        volume_response = ec2_client.create_volume(
            AvailabilityZone=az,
            Size=10,  # Size in GiB
            VolumeType='gp2',  # General Purpose SSD
            TagSpecifications=[
                {
                    'ResourceType': 'volume',
                    'Tags': [{'Key': 'Name', 'Value': 'MyVolume'}]
                }
            ]
        )
        volume_id = volume_response['VolumeId']
        attach_response = ec2_client.attach_volume(
            VolumeId=volume_id,
            InstanceId=instance_id,
            Device='/dev/sdf'  # Adjust device name as needed
        )
        attach_msg = f"Attached volume '{volume_id}' to instance '{instance_id}'."
        print(attach_msg)
        logging.info(attach_msg)

    except Exception as e:
        volume_error_msg = f"Failed to create or attach volume: {str(e)}"
        print(volume_error_msg)
        logging.error(volume_error_msg)
    

except Exception as e:
    error_msg = f"Failed to launch EC2 instance: {str(e)}"
    print(error_msg)
    logging.error(error_msg)
    


    


# Note: Ensure that the instance is in a state that allows volume attachment (e.g., running).

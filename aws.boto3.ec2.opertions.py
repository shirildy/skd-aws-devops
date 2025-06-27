#create an EC2 client and list all the instance in my account 

import boto3
# Create a session using the default profile
session = boto3.Session(profile_name='default')
# Create an EC2 client
ec2_client = session.client('ec2', region_name='ap-southeast-2')

key_pair_name = 'aws-boto3-key-pair'

try:
    ec2_client.describe_key_pairs(KeyNames=[key_pair_name])
    print(f"Key Pair '{key_pair_name}' already exists.")
except ec2_client.exceptions.ClientError as e:
    if 'InvalidKeyPair.NotFound' in str(e):
        # Create a new key pair if it does not exist
        response = ec2_client.create_key_pair(KeyName=key_pair_name)
        print("Key Pair Created:")
        print(response['KeyMaterial'])
else:
    raise


# response = ec2_client.create_key_pair(KeyName='aws-boto3-key-pair')
# print("Key Pair Created:")
# print(response['KeyMaterial'])  

# List all key pairs
key_pairs = ec2_client.describe_key_pairs()
print("Key Pairs:")
for key_pair in key_pairs['KeyPairs']:
    print(f"  - {key_pair['KeyName']}") 






#create a new EC2 instance (replace 'ami-12345678' with a valid AMI ID)
# response = ec2_client.run_instances(
#     ImageId='ami-12345678',  # Replace with a valid AMI ID
#     InstanceType='t2.micro',  # Replace with the desired instance type
#     MinCount=1,  # Minimum number of instances to launch
#     MaxCount=1,  # Maximum number of instances to launch
#     KeyName='your-key-pair-name',  # Replace with your key pair name
#     SecurityGroupIds=['sg-12345678'],  # Replace with your security group ID
#     SubnetId='subnet-12345678'  # Replace with your subnet ID
# )
# Note: The above code to create an EC2 instance is commented out.

# response = ec2_client.run_instances(
#     ImageId='ami-12345678',  # Replace with a valid AMI ID
#     InstanceType='t2.micro',  # Replace with the desired instance type
#     MinCount=1,  # Minimum number of instances to launch
#     MaxCount=1,  # Maximum number of instances to launch
#     KeyName='your-key-pair-name',  # Replace with your key pair name
#     SecurityGroupIds=['sg-12345678'],  # Replace with your security group ID
#     SubnetId='subnet-12345678'  # Replace with your subnet ID
# )


# List all EC2 instances
# response = ec2_client.describe_instances()
# instances = response['Reservations'][0]['Instances']
# print("EC2 Instances:")
# for instance in instances:
#     print(f"  - {instance['InstanceId']}")
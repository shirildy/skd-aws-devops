import boto3

def create_volume_from_subnet(ec2_client, subnet_id, size_gib=10, volume_type='gp2', tag_key='Name', tag_value='MyVolume'):
    # Step 1: Find the Availability Zone from subnet
    subnet_info = ec2_client.describe_subnets(SubnetIds=[subnet_id])
    az = subnet_info['Subnets'][0]['AvailabilityZone']

    # Step 2: Create the volume in the same AZ
    volume_response = ec2_client.create_volume(
        AvailabilityZone=az,
        Size=size_gib,
        VolumeType=volume_type,
        TagSpecifications=[
            {
                'ResourceType': 'volume',
                'Tags': [{'Key': tag_key, 'Value': tag_value}]
            }
        ]
    )

    return volume_response

def attach_volume_to_instance(ec2_client, volume_id, instance_id, device='/dev/sdf'):
    # Wait for volume to be available
    volume_waiter = ec2_client.get_waiter('volume_available')
    volume_waiter.wait(VolumeIds=[volume_id])
    


    attach_response = ec2_client.attach_volume(
        VolumeId=volume_id,
        InstanceId=instance_id,
        Device=device
    )

    return attach_response
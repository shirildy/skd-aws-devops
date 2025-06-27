
#prerequisites:
# 1. Install Boto3: pip install boto3
# 2. Configure AWS credentials: aws configure
#    - Enter your AWS Access Key ID
#    - Enter your AWS Secret Access Key
#    - Enter your default region name (e.g., us-west-2)
# 3. Ensure you have the necessary permissions to create and list S3 buckets.
# 4. Make sure you have Python installed on your system.
# 5. Ensure you have the necessary permissions to create and list S3 buckets.
# 6. Ensure you have the necessary permissions to copy objects in S3 buckets.
# 7. Ensure you have the necessary permissions to rename S3 buckets.
# 8. Ensure you have the necessary permissions to delete S3 buckets.
# 9. Ensure you have the necessary permissions to list S3 buckets.
# 10. Ensure you have the necessary permissions to delete objects in S3 buckets.
# 11. Ensure you have the necessary permissions to list objects in S3 buckets.
# 12. Ensure you have the necessary permissions to get bucket location.
# 13. Ensure you have the necessary permissions to get bucket policy.
# 14. Ensure you have the necessary permissions to put bucket policy.
# 15. Ensure you have the necessary permissions to get bucket versioning.






# This script demonstrates how to use the Boto3 library to interact with AWS services.
import boto3    
      
# Create a session using the default profile
session = boto3.Session(profile_name='default')

# Create an S3 client
s3_client = session.client('s3', region_name='ap-southeast-2')


# Create a new bucket (replace 'your-new-bucket-name' with a unique bucket name) 
# new_bucket_name = 'skd-dev04'
# s3_client.create_bucket(
#     Bucket=new_bucket_name,
#     CreateBucketConfiguration={'LocationConstraint': 'ap-southeast-2'}
# )



# List all buckets
buckets = s3_client.list_buckets()
print("Buckets:")
for bucket in buckets['Buckets']:
    print(f"  - {bucket['Name']}")


#Rename the existing bucket- add loop index no as prefix
# for i, bucket in enumerate(buckets['Buckets']):
#     new_name = f"skd-dev04-{i}"
#     s3_client.copy_object(
#         ACL='private',
#         Bucket=bucket['Name'],
#         CopySource={'Bucket': bucket['Name'], 'Key': ''},
#         Key=new_name
#     )

# List all buckets
buckets = s3_client.list_buckets()
print("Buckets:")
for bucket in buckets['Buckets']:
    print(f"  - {bucket['Name']}")

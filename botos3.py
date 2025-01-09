import boto3
import os
import requests

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'Default Value')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'Default Value')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', 'Default Value')

# Initialize the S3 client
client = boto3.client('s3')

try:
    bucket_name = "suba-bucket"
    # Create the S3 bucket
    response = client.create_bucket(
        Bucket=bucket_name,
        #ObjectLockEnabledForBucket=False,
        ObjectOwnership='BucketOwnerPreferred'
    )
    #puclic access unblock panna
    response = client.delete_public_access_block(
        Bucket=bucket_name,
        ExpectedBucketOwner='890742598563'
    )

       print("Bucket created successfully:", response)
except :
    print("Error creating bucket:")


# webpage source code
#url = "https://dev.to/" 
url = os.getenv('URL', 'Default Value')
print(f"Enter the URL: {url}")
response = requests.get(url)
response.raise_for_status() 
if response.status_code == 200:
    webpage_content = response.text
else:
    print("Failed to retrieve the webpage")
    exit()

#  Save the content with UTF-8 encoding
file_name = "source.html"
with open(file_name, "w", encoding="utf-8") as file:
    file.write(webpage_content)


# Upload the file to S3
s3 = boto3.client('s3')
bucket_name = bucket_name  

try:
    #s3.upload_file(file_name, bucket_name, file_name)
    s3.upload_file(file_name, bucket_name, file_name, ExtraArgs={'ACL': 'public-read', 'ContentType': 'text/html'})
    print(f"File {file_name} uploaded to S3 successfully!")
except:
    print(f"Error uploading file to S3")

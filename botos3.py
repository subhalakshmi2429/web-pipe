import boto3
import os
import requests

# Get the AWS credentials and region from environment variables
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID','Default Value')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY','Default Value')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION','Default Value')

# Initialize the S3 client
client = boto3.client('s3', 
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_DEFAULT_REGION)

try:
    bucket_name = "jenkin_bucket"
    
    # Create the S3 bucket
    response = client.create_bucket(
        Bucket=bucket_name,
        ObjectOwnership='BucketOwnerPreferred'
    )
    
    # Unblock public access
    response = client.delete_public_access_block(
        Bucket=bucket_name,
        ExpectedBucketOwner='890742598563'
    )

    print("Bucket created successfully:", response)
except Exception as e:
    print(f"Error creating bucket: {e}")

# Fetch webpage content
url = os.getenv('URL', 'https://dev.to/')  # Default URL in case URL is not set
print(f"Enter the URL: {url}")
response = requests.get(url)

try:
    response.raise_for_status()  # Will raise an exception for non-200 responses
    if response.status_code == 200:
        webpage_content = response.text
    else:
        print("Failed to retrieve the webpage")
        exit()
except requests.exceptions.RequestException as e:
    print(f"Error fetching webpage: {e}")
    exit()

# Save the content with UTF-8 encoding
file_name = "source.html"
with open(file_name, "w", encoding="utf-8") as file:
    file.write(webpage_content)

# Upload the file to S3
s3 = boto3.client('s3', 
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                  region_name=AWS_DEFAULT_REGION)
try:
    s3.upload_file(file_name, bucket_name, file_name, ExtraArgs={'ACL': 'public-read', 'ContentType': 'text/html'})
    print(f"File {file_name} uploaded to S3 successfully!")
except Exception as e:
    print(f"Error uploading file to S3: {e}")

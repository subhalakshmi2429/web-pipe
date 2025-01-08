import os
import boto3
import requests

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'Default Value')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'Default Value')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', 'Default Value')


print(f"\t\t------------ # ------------------ # ------------------ # --------------- # -------------- # ---------")
print(f"\t\t\t WELCOME TO PYTHON(BOTO3) SCRIPT USE TO CREATE S3 BUCKET & STATIC WEB HOSTING  ")
print(f"\t\t------------ # ------------------ # ------------------ # --------------- # -------------- # ---------")

# declare the S3 client in boto3
s3_client = boto3.client('s3')

bucket_name = "boto3projectbucket"
#webpage_url = "https://sololearn.com/en/"
file_name = "index.html"

# Function to create an S3 bucket
def create_s3_bucket(bucket_name):
    try:
        s3_client.create_bucket(
            Bucket=bucket_name,
            ObjectOwnership='BucketOwnerPreferred'
        )
        print(f"\n\t\tBucket '{bucket_name}' created successfully.\n")

        # Remove public access block
        s3_client.delete_public_access_block(Bucket=bucket_name)
        print("\t\tPublic access block removed.\n")
        
    except Exception as e:
        print("Error creating bucket:", e)
        return False
    return True

# Function to save webpage content
def save_webpage_content(file_name):
    try:
        url = os.getenv('URL', 'Default Value')
        print(f"Enter the URL : {url}")
        response = requests.get(url)
        response.raise_for_status() 
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f"\t\tWebpage content saved to {file_name}\n")
        return True
    except requests.RequestException as e:
        print("\tFailed to retrieve the webpage:\n\t\t", e)
        return False

# Function to upload a file to S3 with public read access
def upload_file_to_s3(bucket_name, file_name):
    try:
        s3_client.upload_file(
            file_name, bucket_name, file_name,
            ExtraArgs={'ACL': 'public-read', 'ContentType': 'text/html'}
        )
        print(f"\t\tFile '{file_name}' uploaded to bucket '{bucket_name}'.\n")
        print(f"\t\t\t--------------------------------------------------------------------------------")
        print(f"\t\t\t| The URL is : https://{bucket_name}.s3.us-east-1.amazonaws.com/{file_name} |")
        print(f"\t\t\t--------------------------------------------------------------------------------\n\n")

        print(f"\t\t------------ # ------------------ # ------------------ # --------------- # -------------- # ---------")
        print(f"\t\t\t\t SCRIPT EXECUTED SUCCESSFULLY KINDLY CHECK THE URL, THANK YOU :)  ")
        print(f"\t\t------------ # ------------------ # ------------------ # --------------- # -------------- # ---------")
    except Exception as e:
        print("\tError uploading file to S3:\n\t\t", e)

#Function call
if create_s3_bucket(bucket_name):
    if save_webpage_content(file_name):
        upload_file_to_s3(bucket_name, file_name)


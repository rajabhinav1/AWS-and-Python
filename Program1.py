import boto3
import sys
from datetime import datetime
import random
import string

def create_unique_bucket_name(base_name):
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{base_name}_{random_suffix}"

def file_exists_for_date(s3_client, bucket_name, date):
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    for obj in response.get('Contents', []):
        last_modified = obj['LastModified']
        if last_modified.date() == date:
            return True
    return False

def main(date_str):
    # Configure AWS S3
    s3_client = boto3.client('s3')
    
    # Create a unique bucket name
    bucket_name = create_unique_bucket_name("file_not_uploaded")
    
    # Create the bucket
    s3_client.create_bucket(Bucket=bucket_name)

    # Upload a file
    s3_client.upload_file('example.txt', bucket_name, 'example.txt')

    # Convert string to date
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    # Check if file exists for the given date
    if file_exists_for_date(s3_client, bucket_name, date):
        print(f"1 file found for {date_str}")
    else:
        print(f"[Error] No file found for {date_str}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./file_not_uploaded.py <YYYY-MM-DD>")
        sys.exit(1)
    
    main(sys.argv[1])

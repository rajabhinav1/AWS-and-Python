import boto3
from datetime import datetime, timedelta

def delete_old_images(ecr_client, repository_name, retain_count, older_than_days):
    # Get list of image details
    response = ecr_client.describe_images(repositoryName=repository_name)
    images = response['imageDetails']

    # Sort images by date
    images.sort(key=lambda x: x['imagePushedAt'], reverse=True)

    # Retain the last 'retain_count' images
    images_to_keep = images[:retain_count]
    images_to_check = images[retain_count:]

    # Date to compare
    compare_date = datetime.now() - timedelta(days=older_than_days)

    # Filter out images older than 'older_than_days'
    images_to_delete = [image for image in images_to_check if image['imagePushedAt'] < compare_date]

    # Delete old images
    for image in images_to_delete:
        image_id = {'imageDigest': image['imageDigest']}
        print(f"Deleting image: {image_id}")
        ecr_client.batch_delete_image(repositoryName=repository_name, imageIds=[image_id])

def main():
    ecr_client = boto3.client('ecr')
    repository_name = 'your-ecr-repository-name'  # replace with your ECR repository name
    retain_count = 5
    older_than_days = 30

    delete_old_images(ecr_client, repository_name, retain_count, older_than_days)

if __name__ == '__main__':
    main()

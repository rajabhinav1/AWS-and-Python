import ssl
import socket
import datetime
import requests
from urllib.parse import urlparse

def check_cert_expiry(url, days_threshold, slack_webhook_url):
    # Parse the domain name from the URL
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # Establish a connection to get certificate details
    context = ssl.create_default_context()
    with socket.create_connection((domain, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=domain) as ssock:
            cert = ssock.getpeercert()

    # Extract expiry date and calculate remaining days
    expiry_date = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
    current_date = datetime.datetime.now()
    days_remaining = (expiry_date - current_date).days

    # Check if certificate is expiring within the threshold
    if days_remaining <= days_threshold:
        message = f"Alert: SSL certificate for {url} is expiring in {days_remaining} days."
        payload = {"text": message}
        requests.post(slack_webhook_url, json=payload)

def main():
    # Sample website
    sample_url = "https://www.example.com"
    
    # Days threshold
    days_threshold = 30  # Number of days to check for expiry

    # Slack Webhook URL
    slack_webhook_url = "YOUR_SLACK_WEBHOOK_URL"  # Replace with your Slack Webhook URL

    check_cert_expiry(sample_url, days_threshold, slack_webhook_url)

if __name__ == "__main__":
    main()

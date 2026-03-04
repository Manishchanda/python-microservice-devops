import json
import os

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from flask import Flask, jsonify

app = Flask(__name__)


# Route to the root URL
@app.route("/")
def home():
    return "Hello, World!"


# Route to a custom endpoint
@app.route("/greet/<name>")
def greet(name):
    return f"Hello, {name}! Welcome to Flask on Amazon-ECS."


@app.route("/aws/resources")
def list_s3_buckets():
    # Get credentials from environment variables
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    missing_keys = []
    if not access_key:
        missing_keys.append("AWS_ACCESS_KEY_ID")
    if not secret_key:
        missing_keys.append("AWS_SECRET_ACCESS_KEY")

    if missing_keys:
        error_message = (
            "Missing required AWS credential environment variable(s): "
            + ", ".join(missing_keys)
        )
        app.logger.error(error_message)
        raise RuntimeError(error_message)

    # Create S3 client
    s3 = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )

    # List buckets
    response = s3.list_buckets()

    print("S3 Buckets:\n")
    for bucket in response["Buckets"]:
        print(bucket["Name"])

# def aws_resources():
    region = os.getenv("AWS_REGION", "us-east-1")
    secret_name = os.getenv("AWS_SECRET_NAME")

    session = boto3.session.Session(region_name=region)
    s3_client = session.client("s3")

    try:
        buckets_response = s3_client.list_buckets()
        bucket_names = sorted(
            [bucket["Name"] for bucket in buckets_response.get("Buckets", [])]
        )
    except (ClientError, BotoCoreError) as exc:
        return (
            jsonify(
                {
                    "error": "Failed to list S3 buckets.",
                    "details": str(exc),
                }
            ),
            500,
        )

    secret_data = None
    if secret_name:
        secrets_client = session.client("secretsmanager")
        try:
            secret_value = secrets_client.get_secret_value(SecretId=secret_name)
            if "SecretString" in secret_value:
                secret_string = secret_value["SecretString"]
                try:
                    secret_data = json.loads(secret_string)
                except json.JSONDecodeError:
                    secret_data = {"value": secret_string}
            else:
                secret_data = {"value": "SecretBinary returned (not displayed)."}
        except (ClientError, BotoCoreError) as exc:
            secret_data = {"error": f"Failed to read secret {secret_name}: {str(exc)}"}

    return jsonify(
        {
            "region": region,
            # "secret_name": secret_name,
            # "secret": secret_data,
            "s3_buckets": bucket_names,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)

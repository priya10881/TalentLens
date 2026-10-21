import json
import os
import uuid
import base64

import boto3
from botocore.exceptions import ClientError


# --------------------------------------------------
# AWS CONFIGURATION
# --------------------------------------------------

AWS_REGION = os.environ.get("AWS_REGION", "eu-west-1")
BUCKET_NAME = os.environ.get("RESUME_BUCKET")
TABLE_NAME = os.environ.get(
    "CANDIDATE_TABLE",
    "ResumeScreeningResults"
)

# Allow requests from the local TalentLens frontend.
# If your frontend uses a different port, update this value.
FRONTEND_ORIGIN = "http://localhost:8000"

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION
)

dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION
)

table = dynamodb.Table(TABLE_NAME)


# --------------------------------------------------
# HTTP RESPONSE HELPER
# --------------------------------------------------

def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": FRONTEND_ORIGIN,
            "Access-Control-Allow-Headers": (
                "Content-Type,X-Amz-Date,Authorization,"
                "X-Api-Key,X-Amz-Security-Token"
            ),
            "Access-Control-Allow-Methods": "GET,OPTIONS,POST"
        },
        "body": json.dumps(body)
    }


# --------------------------------------------------
# REQUEST BODY VALIDATION
# --------------------------------------------------

def parse_request_body(event):
    body = event.get("body")

    if not body:
        return None

    if event.get("isBase64Encoded"):
        try:
            body = base64.b64decode(body).decode("utf-8")
        except Exception:
            raise ValueError("Invalid base64 request body")

    if isinstance(body, str):
        body = json.loads(body)

    if not isinstance(body, dict):
        raise ValueError("Request body must be a JSON object")

    return body


# --------------------------------------------------
# MAIN LAMBDA HANDLER
# --------------------------------------------------

def lambda_handler(event, context):

    method = event.get("httpMethod", "")
    path = event.get("path", "")

    # --------------------------------------------------
    # 1. HEALTH CHECK
    # --------------------------------------------------

    if (
        method == "GET"
        and path.rstrip("/").endswith("/health")
    ):
        return response(
            200,
            {
                "message": "Resume Screening API is running!",
                "service": "AWS Lambda",
                "region": AWS_REGION
            }
        )

    # --------------------------------------------------
    # 2. GENERATE PDF UPLOAD URL
    # --------------------------------------------------

    if (
        method == "POST"
        and path.rstrip("/").endswith("/resumes/upload-url")
    ):

        if not BUCKET_NAME:
            return response(
                500,
                {
                    "error": "RESUME_BUCKET environment variable is missing"
                }
            )

        # Parse and validate request body.
        try:
            body = parse_request_body(event)

        except (ValueError, TypeError, json.JSONDecodeError):
            return response(
                400,
                {
                    "error": "Request body must be a valid JSON object"
                }
            )

        if body is None:
            return response(
                400,
                {
                    "error": "Request body is required"
                }
            )

        job_description = body.get("jobDescription", "")

        if not isinstance(job_description, str):
            return response(
                400,
                {
                    "error": "jobDescription must be a string"
                }
            )

        job_description = job_description.strip()

        if not job_description:
            return response(
                400,
                {
                    "error": "jobDescription is required"
                }
            )

        # Create a unique candidate ID and S3 object key.
        candidate_id = str(uuid.uuid4())
        object_key = f"resumes/{candidate_id}.pdf"

        # Generate the presigned S3 upload URL.
        try:
            upload_url = s3.generate_presigned_url(
                "put_object",
                Params={
                    "Bucket": BUCKET_NAME,
                    "Key": object_key,
                    "ContentType": "application/pdf"
                },
                ExpiresIn=300
            )

        except ClientError:
            print("AWS error while generating the upload URL")

            return response(
                500,
                {
                    "error": "Could not generate upload URL"
                }
            )

        # Register the candidate in DynamoDB.
        try:
            table.put_item(
                Item={
                    "candidateId": candidate_id,
                    "jobDescription": job_description,
                    "s3Bucket": BUCKET_NAME,
                    "s3Key": object_key,
                    "screeningStatus": "PENDING_UPLOAD"
                },
                ConditionExpression="attribute_not_exists(candidateId)"
            )

        except ClientError:
            print("AWS error while creating the candidate record")

            return response(
                500,
                {
                    "error": "Could not create candidate record"
                }
            )

        # Return candidate details and upload URL.
        return response(
            200,
            {
                "message": "Upload URL generated successfully",
                "candidateId": candidate_id,
                "bucket": BUCKET_NAME,
                "key": object_key,
                "uploadUrl": upload_url,
                "expiresInSeconds": 300,
                "requiredContentType": "application/pdf",
                "status": "PENDING_UPLOAD"
            }
        )

    # --------------------------------------------------
    # 3. UNKNOWN ROUTE
    # --------------------------------------------------

    return response(
        404,
        {
            "error": "Route not found",
            "path": path,
            "method": method
        }
    )
import os
import json
import boto3
import logging
from pathlib import Path
from tempfile import TemporaryDirectory
from decimal import Decimal
from urllib.parse import unquote_plus

from main import screen_resume

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

TABLE_NAME = os.environ.get("TABLE_NAME", "ResumeScreeningResults")
table = dynamodb.Table(TABLE_NAME)


def convert_floats(value):
    if isinstance(value, float):
        return Decimal(str(value))
    if isinstance(value, dict):
        return {k: convert_floats(v) for k, v in value.items()}
    if isinstance(value, list):
        return [convert_floats(v) for v in value]
    return value


def lambda_handler(event, context):
    results = []

    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        object_key = unquote_plus(record["s3"]["object"]["key"])

        if not object_key.startswith("resumes/") or not object_key.lower().endswith(".pdf"):
            continue

        candidate_id = Path(object_key).stem

        try:
            candidate_response = table.get_item(
                Key={"candidateId": candidate_id}
            )
            candidate = candidate_response.get("Item")

            if not candidate:
                logger.warning("Candidate record not found: %s", candidate_id)
                continue

            if candidate.get("screeningStatus") == "COMPLETED":
                continue

            table.update_item(
                Key={"candidateId": candidate_id},
                UpdateExpression="SET screeningStatus = :status",
                ExpressionAttributeValues={":status": "PROCESSING"}
            )

            job_description = candidate.get("jobDescription", "")

            with TemporaryDirectory() as temp_dir:
                pdf_path = Path(temp_dir) / "resume.pdf"
                s3.download_file(bucket, object_key, str(pdf_path))

                report = screen_resume(pdf_path, job_description)

            if not isinstance(report, dict):
                raise ValueError("Screening did not return a valid report")

            report = convert_floats(report)

            table.update_item(
                Key={"candidateId": candidate_id},
                UpdateExpression=(
                    "SET screeningStatus = :status, "
                    "aiAnalysis = :analysis, "
                    "matchPercentage = :score, "
                    "candidateName = :name, "
                    "matchingSkills = :matching, "
                    "missingSkills = :missing"
                ),
                ExpressionAttributeValues={
                    ":status": "COMPLETED",
                    ":analysis": report,
                    ":score": report.get("matchPercentage", 0),
                    ":name": report.get("candidateName", "Unknown"),
                    ":matching": report.get("matchingSkills", []),
                    ":missing": report.get("missingSkills", [])
                }
            )

            results.append({"candidateId": candidate_id, "status": "COMPLETED"})

        except Exception as exc:
            logger.exception("Screening failed for candidate %s", candidate_id)

            try:
                table.update_item(
                    Key={"candidateId": candidate_id},
                    UpdateExpression="SET screeningStatus = :status, errorMessage = :error",
                    ExpressionAttributeValues={
                        ":status": "FAILED",
                        ":error": str(exc)[:500]
                    }
                )
            except Exception:
                logger.exception("Could not save failure status")

            results.append({"candidateId": candidate_id, "status": "FAILED"})

    return {"statusCode": 200, "body": json.dumps(results)}

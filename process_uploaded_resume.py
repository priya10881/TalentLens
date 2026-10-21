import os
import sys
import tempfile
from pathlib import Path

import boto3

# Existing project modules
from database import get_candidate, update_screening_results

# Location of your existing screening module
SCREENING_DIR = (
    Path.home()
    / "Downloads"
    / "resume-ai-module (2)"
    / "resume-ai-module"
)

sys.path.insert(0, str(SCREENING_DIR))

from main import screen_resume


# AWS configuration
AWS_REGION = "eu-west-1"

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION
)


def process_uploaded_resume(candidate_id):
    """Download a candidate's PDF, screen it, and save the results."""

    candidate = get_candidate(candidate_id)

    if not candidate:
        print("Error: Candidate record not found.")
        return False

    status = candidate.get("screeningStatus")

    if status == "COMPLETED":
        print("This candidate has already been screened.")
        return False

    bucket = candidate.get("s3Bucket")
    object_key = candidate.get("s3Key")
    job_description = candidate.get("jobDescription")

    if not bucket or not object_key or not job_description:
        print("Error: Candidate record is missing required fields.")
        return False

    print("Candidate ID:", candidate_id)
    print("Downloading resume from S3...")

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_path = Path(temp_dir) / "resume.pdf"

            s3.download_file(
                bucket,
                object_key,
                str(pdf_path)
            )

            print("PDF downloaded successfully.")
            print("Running resume screening...")

            report = screen_resume(
                pdf_path,
                job_description
            )

            if not isinstance(report, dict):
                print("Error: Resume screening did not return a report.")
                return False

            print("Screening completed.")
            print("Match percentage:", report.get("matchPercentage"))

            # Update the existing candidate record.
            success = update_screening_results(
                candidate_id,
                report
            )

            if success:
                print("Candidate record updated successfully.")
                print("Final status: COMPLETED")

            return success

    except Exception as error:
        print("Error processing resume:", error)
        return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Usage: python process_uploaded_resume.py <candidate_id>"
        )
        raise SystemExit(1)

    candidate_id = sys.argv[1].strip()

    if not candidate_id:
        print("Candidate ID cannot be empty.")
        raise SystemExit(1)

    success = process_uploaded_resume(candidate_id)

    if not success:
        raise SystemExit(1)

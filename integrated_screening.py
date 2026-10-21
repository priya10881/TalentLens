import sys
from pathlib import Path
from uuid import uuid4

# Locate Member 2's project
MEMBER2_PATH = (
    Path.home()
    / "Downloads"
    / "resume-ai-module (2)"
    / "resume-ai-module"
)

if not MEMBER2_PATH.is_dir():
    raise FileNotFoundError(
        f"Member 2's project folder was not found: {MEMBER2_PATH}"
    )

sys.path.insert(0, str(MEMBER2_PATH))

from main import screen_resume
from database import save_candidate
from candidate_service import get_candidate_details


def screen_and_save_resume(
    pdf_path,
    job_description,
    github_username=None
):
    """Screen a resume and save its report to DynamoDB."""

    # Step 1: Screen the resume
    report = screen_resume(pdf_path, job_description)

    if not report:
        print("Resume screening failed. Nothing was saved.")
        return None

    # Step 2: Add a unique candidate ID
    report["candidateId"] = f"CAND-{uuid4().hex[:12].upper()}"

    report["githubUsername"] = (
        github_username.strip()
        if github_username and github_username.strip()
        else None
    )

    report["screeningStatus"] = "Completed"

    # Step 3: Save the report
    success = save_candidate(report)

    if not success:
        print("Could not save the screening report to DynamoDB.")
        return None

    print("\nScreening report saved successfully!")
    print(f"Candidate ID: {report['candidateId']}")

    return report["candidateId"]


def retrieve_candidate(candidate_id):
    """Retrieve a candidate and available GitHub details."""
    return get_candidate_details(candidate_id)


if __name__ == "__main__":

    print("=== Integrated Resume Screening ===")

    pdf_path = input(
        "Enter the full path to the resume PDF: "
    ).strip()

    job_description = input(
        "Paste the job description: "
    ).strip()

    github_username = input(
        "Enter GitHub username (or press Enter to skip): "
    ).strip()

    candidate_id = screen_and_save_resume(
        pdf_path,
        job_description,
        github_username or None
    )

    if candidate_id:
        print("\nScreening workflow completed!")
        print(f"Candidate ID: {candidate_id}")

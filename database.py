import boto3
from decimal import Decimal
from botocore.exceptions import ClientError, BotoCoreError


# ============================================================
# AWS CONFIGURATION
# ============================================================

REGION = "eu-west-1"
TABLE_NAME = "ResumeScreeningResults"

dynamodb = boto3.resource(
    "dynamodb",
    region_name=REGION
)

table = dynamodb.Table(TABLE_NAME)


# ============================================================
# CONVERT FLOATS TO DECIMAL
# ============================================================

def convert_floats_to_decimal(value):
    """Convert floats recursively to Decimal for DynamoDB."""

    if isinstance(value, float):
        return Decimal(str(value))

    if isinstance(value, dict):
        return {
            key: convert_floats_to_decimal(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            convert_floats_to_decimal(item)
            for item in value
        ]

    if isinstance(value, tuple):
        return [
            convert_floats_to_decimal(item)
            for item in value
        ]

    return value


# ============================================================
# SAVE A NEW CANDIDATE
# ============================================================

def save_candidate(candidate):
    """
    Save a new candidate record.

    Returns True on success and False on failure.
    """

    if not isinstance(candidate, dict):
        print("Error: Candidate data must be a dictionary.")
        return False

    candidate_id = candidate.get("candidateId")

    if not isinstance(candidate_id, str) or not candidate_id.strip():
        print("Error: A valid candidateId is required.")
        return False

    candidate_to_save = convert_floats_to_decimal(candidate)

    try:
        table.put_item(
            Item=candidate_to_save,
            ConditionExpression="attribute_not_exists(candidateId)"
        )

        print("Candidate saved successfully!")
        return True

    except ClientError as error:
        code = error.response.get("Error", {}).get("Code")

        if code == "ConditionalCheckFailedException":
            print("Candidate ID already exists.")
        else:
            print("Error saving candidate:", error)

        return False

    except BotoCoreError as error:
        print("AWS connection error:", error)
        return False

    except (TypeError, ValueError) as error:
        print("Invalid candidate data:", error)
        return False


# ============================================================
# RETRIEVE AN EXISTING CANDIDATE
# ============================================================

def get_candidate(candidate_id):
    """
    Retrieve a candidate by ID.

    Returns the candidate dictionary or None.
    """

    if not isinstance(candidate_id, str) or not candidate_id.strip():
        print("Error: Candidate ID cannot be empty.")
        return None

    try:
        result = table.get_item(
            Key={
                "candidateId": candidate_id.strip()
            },
            ConsistentRead=True
        )

        return result.get("Item")

    except (ClientError, BotoCoreError) as error:
        print("Error retrieving candidate:", error)
        return None


# ============================================================
# UPDATE EXISTING SCREENING RESULTS
# ============================================================

def update_screening_results(candidate_id, screening_report):
    """
    Update an existing candidate with screening results.

    The original candidate ID and S3 information are preserved.
    The screening status becomes COMPLETED after a successful update.
    """

    if not isinstance(candidate_id, str) or not candidate_id.strip():
        print("Error: A valid candidate ID is required.")
        return False

    if not isinstance(screening_report, dict):
        print("Error: Screening report must be a dictionary.")
        return False

    # Make a copy so the caller's report is not modified.
    report = dict(screening_report)

    # Do not allow the report to change the primary key or S3 location.
    report.pop("candidateId", None)
    report.pop("s3Bucket", None)
    report.pop("s3Key", None)
    report.pop("screeningStatus", None)

    if not report:
        print("Error: Screening report contains no results to update.")
        return False

    # Convert floats, including nested values inside AI analysis.
    report = convert_floats_to_decimal(report)

    try:
        # Build the update expression.
        expression_names = {
            "#status": "screeningStatus"
        }

        expression_values = {
            ":status": "COMPLETED"
        }

        update_parts = [
            "#status = :status"
        ]

        for index, (key, value) in enumerate(report.items()):
            name_placeholder = f"#field{index}"
            value_placeholder = f":value{index}"

            expression_names[name_placeholder] = key
            expression_values[value_placeholder] = value

            update_parts.append(
                f"{name_placeholder} = {value_placeholder}"
            )

        table.update_item(
            Key={
                "candidateId": candidate_id.strip()
            },
            UpdateExpression="SET " + ", ".join(update_parts),
            ExpressionAttributeNames=expression_names,
            ExpressionAttributeValues=expression_values,
            ConditionExpression="attribute_exists(candidateId)"
        )

        print("Screening results updated successfully!")
        return True

    except ClientError as error:
        code = error.response.get("Error", {}).get("Code")

        if code == "ConditionalCheckFailedException":
            print("Error: Candidate record does not exist.")
        else:
            print("Error updating screening results:", error)

        return False

    except BotoCoreError as error:
        print("AWS connection error:", error)
        return False

    except (TypeError, ValueError) as error:
        print("Invalid screening report:", error)
        return False


# ============================================================
# COMMAND-LINE TEST MENU
# ============================================================

if __name__ == "__main__":

    print("===== Resume Screening Database =====")
    print("1. Save a new test candidate")
    print("2. Retrieve a candidate")
    print("3. Update screening results")

    choice = input("Choose an option (1, 2, or 3): ").strip()

    if choice == "1":

        candidate_id = input(
            "Enter a NEW candidate ID: "
        ).strip()

        candidate = {
            "candidateId": candidate_id,
            "candidateName": "Test Candidate",
            "email": "test@example.com",
            "skills": ["Python", "SQL", "AWS"],
            "githubUsername": "octocat",
            "screeningStatus": "TEST"
        }

        if candidate_id:
            save_candidate(candidate)
        else:
            print("Candidate ID cannot be empty.")

    elif choice == "2":

        candidate_id = input(
            "Enter candidate ID: "
        ).strip()

        candidate = get_candidate(candidate_id)

        if candidate:
            print("\nCandidate found!")
            print(candidate)
        else:
            print("\nCandidate not found, or retrieval failed.")

    elif choice == "3":

        candidate_id = input(
            "Enter an EXISTING candidate ID: "
        ).strip()

        screening_report = {
            "matchPercentage": 85.0,
            "matchingSkills": [
                "Python",
                "AWS",
                "DynamoDB"
            ],
            "missingSkills": [
                "Docker"
            ],
            "suitabilitySummary": (
                "The candidate demonstrates several relevant skills."
            )
        }

        print("\nUpdating screening results...")

        success = update_screening_results(
            candidate_id,
            screening_report
        )

        if success:
            print("\nUpdated candidate:")
            print(get_candidate(candidate_id))

    else:
        print("Invalid choice.")

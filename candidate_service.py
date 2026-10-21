from database import get_candidate
from github_api import get_github_profile, get_github_repositories


def get_candidate_details(candidate_id):
    # Step 1: Retrieve candidate from DynamoDB
    candidate = get_candidate(candidate_id)

    if not candidate:
        return {"error": "Candidate not found in DynamoDB"}

    # Step 2: Get their GitHub username
    username = candidate.get("githubUsername")

    result = {
        "candidate": candidate,
        "githubProfile": None,
        "githubRepositories": None
    }

    # Step 3: Fetch GitHub information if a username exists
    if username:
        result["githubProfile"] = get_github_profile(username)
        result["githubRepositories"] = get_github_repositories(username)

    return result


if __name__ == "__main__":
    candidate_id = input("Enter candidate ID: ").strip()

    details = get_candidate_details(candidate_id)

    print("\n--- Candidate Details ---")
    print(details)
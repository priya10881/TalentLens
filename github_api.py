import requests


def get_github_profile(username):
    """Fetch a candidate's public GitHub profile."""

    url = f"https://api.github.com/users/{username}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 404:
            return {"error": "GitHub user not found"}

        response.raise_for_status()
        data = response.json()

        return {
            "username": data.get("login"),
            "name": data.get("name"),
            "public_repos": data.get("public_repos"),
            "followers": data.get("followers"),
            "profile_url": data.get("html_url")
        }

    except requests.RequestException as error:
        return {"error": str(error)}


def get_github_repositories(username):
    """Fetch a candidate's public repositories."""

    url = f"https://api.github.com/users/{username}/repos"

    try:
        response = requests.get(
            url,
            params={"per_page": 10, "sort": "updated"},
            timeout=10
        )

        if response.status_code == 404:
            return {"error": "GitHub user not found"}

        response.raise_for_status()

        repositories = []

        for repo in response.json():
            repositories.append({
                "name": repo.get("name"),
                "description": repo.get("description"),
                "language": repo.get("language"),
                "url": repo.get("html_url")
            })

        return repositories

    except requests.RequestException as error:
        return {"error": str(error)}


if __name__ == "__main__":
    username = input("Enter GitHub username: ").strip()

    if not username:
        print("Please enter a GitHub username.")
    else:
        print("\n--- GitHub Profile ---")
        print(get_github_profile(username))

        print("\n--- Public Repositories (up to 10) ---")
        print(get_github_repositories(username))
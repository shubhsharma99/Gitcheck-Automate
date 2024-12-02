from github import Github

# GitHub credentials
GITHUB_TOKEN = "your_personal_access_token"  # Replace with your GitHub PAT
REPO_NAME = "username/repository_name"  # Replace with your repository (e.g., "user/repo")

# Initialize GitHub object
g = Github(GITHUB_TOKEN)

# Get the repository
repo = g.get_repo(REPO_NAME)

# Step 1: Configure branch protection rules for the 'master' branch
branch = repo.get_branch("master")
protection_rules = {
    "required_status_checks": {
        "strict": True,
        "contexts": ["Pull Request Checks"],  # Contexts added after the workflow runs
    },
    "enforce_admins": True,
    "required_pull_request_reviews": {
        "dismissal_restrictions": {},  # Empty for no restrictions
        "dismiss_stale_reviews": True,
        "require_code_owner_reviews": True,
        "required_approving_review_count": 1,
    },
    "restrictions": None,  # No restrictions on who can push
}

branch.edit_protection(
    required_status_checks=protection_rules["required_status_checks"],
    enforce_admins=protection_rules["enforce_admins"],
    required_pull_request_reviews=protection_rules["required_pull_request_reviews"],
    restrictions=protection_rules["restrictions"]
)
print("Branch protection rules applied successfully.")

# Step 2: Create a GitHub Actions workflow for pull request checks
workflow_file_content = """
name: Pull Request Checks

on:
  pull_request:
    branches:
      - master

jobs:
  checks:
    name: Run Checks
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run Linting
        run: |
          pip install flake8
          flake8 .

      - name: Run Tests
        run: |
          pip install pytest
          pytest
"""

# Add the workflow file to the repository
file_path = ".github/workflows/pull-request-checks.yml"
try:
    repo.create_file(
        path=file_path,
        message="Add workflow for pull request checks",
        content=workflow_file_content,
        branch="master"
    )
    print(f"Workflow file '{file_path}' created successfully.")
except Exception as e:
    print(f"Error creating workflow file: {e}")


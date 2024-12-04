from github import Github

# GitHub credentials
GITHUB_TOKEN = "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"  # Replace with your GitHub PAT
REPO_NAME = "shubhsharma99/Gitcheck-Automate"  # Replace with your repository (e.g., "user/repo")
BRANCH_NAME = "main"  # Replace with your desired branch name (e.g., "main", "develop")

# Initialize the GitHub client
g = Github(GITHUB_TOKEN)

# Get the repository
repo = g.get_repo(REPO_NAME)

# Get the branch to protect
branch = repo.get_branch(BRANCH_NAME)

# Configure the protection rules
protection_rules = {
    "required_status_checks": {
        "strict": True,
        "contexts": ["ci/circleci", "lint"],  # Example contexts (adjust based on your CI tools)
    },
    "enforce_admins": True,  # Enforce protection even for admins
    "required_pull_request_reviews": {
        "dismiss_stale_reviews": True,  # Dismiss stale reviews
        "require_code_owner_reviews": True,  # Require code owner reviews
        "required_approving_review_count": 1,  # Minimum 1 approval
    },
    "restrictions": {
        "users": ["specific-user"],  # Only these users can push to the branch (optional)
        "teams": ["specific-team"],  # Only these teams can push to the branch (optional)
    },
}

# Apply the protection rules
branch.edit_protection(
    required_status_checks=protection_rules["required_status_checks"],
    enforce_admins=protection_rules["enforce_admins"],
    required_pull_request_reviews=protection_rules["required_pull_request_reviews"],
    restrictions=protection_rules["restrictions"]
)

print(f"Protection rules applied successfully to '{BRANCH_NAME}' branch.")

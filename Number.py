import os
import subprocess
import requests

# GitHub Configuration (replace with your GitHub details)
GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = "your-github-token"  # Replace with your GitHub personal access token
ORGANIZATION_NAME = "your-organization-name"  # Replace with your GitHub organization name

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
OUTPUT_DIR = os.path.join(BASE_DIR, "generated")
VARS_DIR = os.path.join(OUTPUT_DIR, "vars")
GIT_SCRIPT = os.path.join(BASE_DIR, "git-pipeline.sh")

# Ensure directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(VARS_DIR, exist_ok=True)

# Function to run the Git pipeline script
def run_git_pipeline():
    try:
        subprocess.run(["bash", GIT_SCRIPT], check=True)
        print("Git pipeline executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing git-pipeline.sh: {e}")

# Function to fetch repositories for the organization
def fetch_organization_repositories():
    try:
        response = requests.get(
            f"{GITHUB_API_URL}/orgs/{ORGANIZATION_NAME}/repos",
            headers={"Authorization": f"token {GITHUB_TOKEN}"}
        )
        response.raise_for_status()
        repos = response.json()
        return [repo["name"] for repo in repos]
    except requests.RequestException as e:
        print(f"Error fetching repositories for organization '{ORGANIZATION_NAME}': {e}")
        return []

# Function to clone a GitHub repository
def clone_repository(repo_name):
    repo_url = f"https://github.com/{ORGANIZATION_NAME}/{repo_name}.git"
    clone_path = os.path.join(OUTPUT_DIR, repo_name)
    try:
        subprocess.run(["git", "clone", repo_url, clone_path], check=True)
        print(f"Cloned repository {repo_name} into {clone_path}.")
        return clone_path
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        return None

# Function to copy generated files into the repository
def copy_generated_files(repo_path):
    try:
        for file_name in os.listdir(OUTPUT_DIR):
            file_path = os.path.join(OUTPUT_DIR, file_name)
            if os.path.isfile(file_path):
                subprocess.run(["cp", file_path, repo_path], check=True)
        print(f"Copied generated files into {repo_path}.")
    except Exception as e:
        print(f"Error copying files: {e}")

# Function to handle GitHub operations
def handle_github_operations():
    user_choice = input("Do you want to create a new GitHub repository? (y/n): ").strip().lower()

    if user_choice == "y":
        print("Creating a new GitHub repository...")
        run_git_pipeline()
    elif user_choice == "n":
        print(f"Fetching repositories for organization {ORGANIZATION_NAME}...")
        repos = fetch_organization_repositories()

        if not repos:
            print(f"No repositories found for organization '{ORGANIZATION_NAME}'. Exiting...")
            return

        print("Available repositories:")
        for i, repo_name in enumerate(repos, start=1):
            print(f"{i}. {repo_name}")

        selected_repo_index = int(input("Select a repository by number: ")) - 1
        selected_repo = repos[selected_repo_index]
        print(f"Selected repository: {selected_repo}")

        repo_path = clone_repository(selected_repo)
        if repo_path:
            copy_generated_files(repo_path)
            print("Changes are ready to be committed and pushed.")
        else:
            print("Failed to clone the repository.")
    else:
        print("Invalid input. Exiting...")

# Main function
def main():
    print("Generating Terraform code...")
    # Call your existing Terraform generation logic here

    print("Asking for GitHub operations...")
    handle_github_operations()

if __name__ == "__main__":
    main()

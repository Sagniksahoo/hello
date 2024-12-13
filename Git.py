import os
import subprocess

def clone_repository(repo_name):
    """
    Clones the specified repository and returns its local path.
    """
    ORGANIZATION_NAME = "your_organization_name"  # Replace with your GitHub organization or username
    OUTPUT_DIR = "/path/to/output/directory"  # Replace with the desired directory to clone repos into

    repo_url = f"https://github.com/{ORGANIZATION_NAME}/{repo_name}.git"
    clone_path = os.path.join(OUTPUT_DIR, repo_name)

    try:
        subprocess.run(["git", "clone", repo_url, clone_path], check=True)
        print(f"Cloned repository {repo_name} into {clone_path}.")
        return clone_path
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        return None

def github_sync(repo_path):
    """
    Synchronizes the specified repository with GitHub.
    """
    try:
        # Validate the repository path
        if not os.path.exists(repo_path) or not os.path.isdir(os.path.join(repo_path, ".git")):
            print(f"Error: '{repo_path}' is not a valid Git repository.")
            return

        # Change to the repository directory
        os.chdir(repo_path)

        # Show repository status
        subprocess.run(["git", "status"], check=True)

        # Stage all changes
        subprocess.run(["git", "add", "."], check=True)
        print("Staged all changes.")

        # Prompt user for a commit message
        commit_message = input("Enter commit message: ").strip()

        if not commit_message:
            print("Error: Commit message cannot be empty.")
            return

        # Commit changes
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        print("Committed changes.")

        # Push changes to the remote repository
        subprocess.run(["git", "push"], check=True)
        print("Changes successfully pushed to the remote repository.")

    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
    except Exception as e:
        print(f"Error: {e}")

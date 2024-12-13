import os
import subprocess

def github_sync_and_copy(repo_path, generated_files_path):
    """
    Automatically synchronizes the repository with GitHub, asks for commit comments,
    and merges generated files before committing.
    
    :param repo_path: Path to the local Git repository.
    :param generated_files_path: Path to the directory containing generated files.
    """
    try:
        # Copy generated files to the repository and merge them
        print("Copying and merging generated files...")
        copy_generated_files(repo_path, generated_files_path)  # Use your existing function
        print("Generated files successfully copied and merged.")

        # Change directory to the repository
        os.chdir(repo_path)

        # Validate Git repository
        if not os.path.isdir(".git"):
            print("Error: The specified path is not a valid Git repository.")
            return

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

# Example usage
if __name__ == "__main__":
    repo_path = input("Enter the path to your Git repository: ").strip()
    generated_files_path = input("Enter the path to the directory containing generated files: ").strip()
    github_sync_and_copy(repo_path, generated_files_path)

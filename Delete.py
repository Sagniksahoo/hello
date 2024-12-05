def delete_non_repo_files(generated_path, repo_name):
    """Delete all files and directories from the generated folder except the cloned repository."""
    try:
        for item in os.listdir(generated_path):
            item_path = os.path.join(generated_path, item)

            # Skip the cloned repository folder
            if item == repo_name:
                continue

            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)

        print("Non-repository files deleted successfully.")
    except Exception as e:
        print(f"Error deleting files: {e}")


def main():
    org_name = input("Enter your GitHub organization name: ").strip()
    token = input("Enter your GitHub personal access token: ").strip()

    selected_repo, clone_path = select_repository_and_branch(org_name, token)
    if selected_repo and clone_path:
        # Copy files to the repository folder
        copy_generated_files_to_repo("generated", clone_path)

        # Delete non-repo files from the generated folder
        delete_non_repo_files("generated", selected_repo)

        print(f"Changes are ready to be committed in {clone_path}.")
    else:
        print("No repository or branch selected. Exiting.")


if __name__ == "__main__":
    main()

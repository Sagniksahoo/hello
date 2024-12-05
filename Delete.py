def delete_generated_files(generated_path):
    """Delete all files and directories from the generated folder after copying."""
    try:
        for item in os.listdir(generated_path):
            item_path = os.path.join(generated_path, item)

            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)

        print("Generated files deleted successfully.")
    except Exception as e:
        print(f"Error deleting files: {e}")


def main():
    org_name = input("Enter your GitHub organization name: ").strip()
    token = input("Enter your GitHub personal access token: ").strip()

    selected_repo, clone_path = select_repository_and_branch(org_name, token)
    if selected_repo and clone_path:
        # Copy files to the repository folder
        copy_generated_files_to_repo("generated", clone_path)

        # Delete the copied files
        delete_generated_files("generated")

        print(f"Changes are ready to be committed in {clone_path}.")
    else:
        print("No repository or branch selected. Exiting.")


if __name__ == "__main__":
    main()

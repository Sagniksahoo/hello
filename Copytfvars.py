import os
import shutil

OUTPUT_DIR = "generated"  # This is your base generated folder

def copy_generated_files(repo_name):
    """
    Copy generated files to the repository located inside the 'generated' folder.
    """
    try:
        # Construct the path to the repository
        repo_path = os.path.join(OUTPUT_DIR, repo_name)

        # Check if the repository folder exists
        if not os.path.isdir(repo_path):
            print(f"Repository folder not found: {repo_path}")
            return

        # Ask user if they want to copy specific files
        include_tfvars = input("Do you want to copy the tfvars files? (y/n): ").strip().lower()
        include_locals = input("Do you want to copy the locals.tf file? (y/n): ").strip().lower()
        include_data = input("Do you want to copy the data.tf file? (y/n): ").strip().lower()

        # Validate inputs
        valid_inputs = {"y", "n"}
        include_tfvars = include_tfvars if include_tfvars in valid_inputs else "n"
        include_locals = include_locals if include_locals in valid_inputs else "n"
        include_data = include_data if include_data in valid_inputs else "n"

        # Iterate over files in OUTPUT_DIR
        for root, _, files in os.walk(OUTPUT_DIR):
            for file_name in files:
                file_path = os.path.join(root, file_name)

                # Skip the repository folder itself
                if repo_name in file_path:
                    continue

                # Construct the destination path within the repository
                relative_path = os.path.relpath(file_path, OUTPUT_DIR)
                destination_path = os.path.join(repo_path, relative_path)

                # Ensure destination directory exists
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)

                # Skip tfvars files if user opted out
                if root.endswith("tfvars") and include_tfvars != "y":
                    print(f"Skipping {file_name} in {root} as per user choice.")
                    continue

                # Skip locals.tf if user opted out
                if file_name == "locals.tf" and include_locals != "y":
                    print(f"Skipping {file_name} as per user choice.")
                    continue

                # Skip data.tf if user opted out
                if file_name == "data.tf" and include_data != "y":
                    print(f"Skipping {file_name} as per user choice.")
                    continue

                # Copy the file
                shutil.copy(file_path, destination_path)
                print(f"Copied {file_name} to {destination_path}.")

        print("All applicable generated files have been copied to the repository.")
    except Exception as e:
        print(f"Error copying files: {e}")

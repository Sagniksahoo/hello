import os
import shutil

def copy_generated_files(repo_path):
    """
    Copy generated files to the specified repository path.
    """
    try:
        # Ensure repo_path exists
        if not os.path.isdir(repo_path):
            print(f"Repository folder not found: {repo_path}")
            return

        # Ask the user about copying specific files
        include_tfvars = input("Do you want to copy the tfvars files? (y/n): ").strip().lower()
        include_locals = input("Do you want to copy the locals.tf file? (y/n): ").strip().lower()
        include_data = input("Do you want to copy the data.tf file? (y/n): ").strip().lower()

        # Validate user input
        valid_inputs = {"y", "n"}
        include_tfvars = include_tfvars if include_tfvars in valid_inputs else "n"
        include_locals = include_locals if include_locals in valid_inputs else "n"
        include_data = include_data if include_data in valid_inputs else "n"

        # Define source folder (output files) and check file copying
        output_dir = "generated"
        for root, _, files in os.walk(output_dir):
            for file_name in files:
                file_path = os.path.join(root, file_name)

                # Skip directories and the repo directory itself
                if repo_path in root:
                    continue

                # Construct the destination path in the repo
                relative_path = os.path.relpath(file_path, output_dir)
                destination_path = os.path.join(repo_path, relative_path)

                # Skip copying tfvars files if user opted out
                if "tfvars" in root and include_tfvars != "y":
                    print(f"Skipping {file_name} in {root} as per user choice.")
                    continue

                # Skip copying locals.tf if user opted out
                if file_name == "locals.tf" and include_locals != "y":
                    print(f"Skipping {file_name} as per user choice.")
                    continue

                # Skip copying data.tf if user opted out
                if file_name == "data.tf" and include_data != "y":
                    print(f"Skipping {file_name} as per user choice.")
                    continue

                # Ensure destination directory exists
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)

                # Copy the file
                shutil.copy(file_path, destination_path)
                print(f"Copied {file_name} to {destination_path}.")

        print("All applicable generated files have been copied to the repository.")

    except Exception as e:
        print(f"Error copying files: {e}")

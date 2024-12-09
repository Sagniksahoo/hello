import os
import shutil

def copy_generated_files(repo_path):
    """
    Copy generated files to the cloned repository with an option to include tfvars files.
    """
    try:
        # Ask user if they want to copy tfvars files
        include_tfvars = input("Do you want to copy the tfvars files? (y/n): ").strip().lower()
        if include_tfvars not in ["y", "n"]:
            print("Invalid input. Skipping tfvars files.")
            include_tfvars = "n"

        # Iterate over files in the OUTPUT_DIR
        for file_name in os.listdir(OUTPUT_DIR):
            file_path = os.path.join(OUTPUT_DIR, file_name)
            destination_path = os.path.join(repo_path, file_name)

            # Copy files only, skip directories
            if os.path.isfile(file_path):
                # Skip tfvars files if user opted out
                if not include_tfvars == "y" and file_name.endswith(".tfvars"):
                    print(f"Skipping {file_name} as per user choice.")
                    continue

                # Copy the file
                shutil.copy(file_path, destination_path)
                print(f"Copied {file_name} to {destination_path}.")

        print("All applicable generated files have been copied to the repository.")
    except Exception as e:
        print(f"Error copying files: {e}")

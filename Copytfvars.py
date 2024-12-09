import os
import shutil

def copy_generated_files(repo_path):
    """
    Copy generated files to the cloned repository with options to skip tfvars, locals.tf, and data.tf files.
    """
    try:
        # Ask user if they want to copy specific files
        include_tfvars = input("Do you want to copy the tfvars files? (y/n): ").strip().lower()
        include_locals = input("Do you want to copy the locals.tf file? (y/n): ").strip().lower()
        include_data = input("Do you want to copy the data.tf file? (y/n): ").strip().lower()

        # Validate inputs
        valid_inputs = {"y", "n"}
        if include_tfvars not in valid_inputs:
            print("Invalid input for tfvars. Skipping tfvars files.")
            include_tfvars = "n"
        if include_locals not in valid_inputs:
            print("Invalid input for locals.tf. Skipping locals.tf.")
            include_locals = "n"
        if include_data not in valid_inputs:
            print("Invalid input for data.tf. Skipping data.tf.")
            include_data = "n"

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

                # Skip locals.tf if user opted out
                if not include_locals == "y" and file_name == "locals.tf":
                    print(f"Skipping {file_name} as per user choice.")
                    continue

                # Skip data.tf if user opted out
                if not include_data == "y" and file_name == "data.tf":
                    print(f"Skipping {file_name} as per user choice.")
                    continue

                # Copy the file
                shutil.copy(file_path, destination_path)
                print(f"Copied {file_name} to {destination_path}.")

        print("All applicable generated files have been copied to the repository.")
    except Exception as e:
        print(f"Error copying files: {e}")

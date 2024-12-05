import shutil

def copy_generated_files_and_clean(repo_path):
    try:
        # Iterate over items in the OUTPUT_DIR
        for item_name in os.listdir(OUTPUT_DIR):
            item_path = os.path.join(OUTPUT_DIR, item_name)
            destination_path = os.path.join(repo_path, item_name)

            # Copy directories
            if os.path.isdir(item_path):
                if os.path.exists(destination_path):
                    shutil.rmtree(destination_path)  # Remove existing directory to avoid conflicts
                shutil.copytree(item_path, destination_path)
                print(f"Copied folder {item_name} to {destination_path}.")
                # Delete the source directory after copying
                shutil.rmtree(item_path)
                print(f"Deleted folder {item_name} from {OUTPUT_DIR}.")
            # Copy files
            elif os.path.isfile(item_path):
                shutil.copy(item_path, destination_path)
                print(f"Copied file {item_name} to {destination_path}.")
                # Delete the source file after copying
                os.remove(item_path)
                print(f"Deleted file {item_name} from {OUTPUT_DIR}.")
        print("All generated files and folders have been copied to the repository and deleted from the output directory.")
    except Exception as e:
        print(f"Error copying and deleting files: {e}")

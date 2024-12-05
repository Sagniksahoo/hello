import shutil

def copy_generated_files(repo_path):
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
            # Copy files
            elif os.path.isfile(item_path):
                shutil.copy(item_path, destination_path)
                print(f"Copied file {item_name} to {destination_path}.")
        print("All generated files and folders have been copied to the repository.")
    except Exception as e:
        print(f"Error copying files and folders: {e}")

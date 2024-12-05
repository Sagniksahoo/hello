import shutil

def copy_generated_files(repo_path):
    try:
        # Iterate over files in the OUTPUT_DIR
        for file_name in os.listdir(OUTPUT_DIR):
            file_path = os.path.join(OUTPUT_DIR, file_name)
            destination_path = os.path.join(repo_path, file_name)
            
            # Copy only files, skip directories
            if os.path.isfile(file_path):
                shutil.copy(file_path, destination_path)
                print(f"Copied {file_name} to {destination_path}.")
        print("All generated files have been copied to the repository.")
    except Exception as e:
        print(f"Error copying files: {e}")

def copy_generated_files(repo_path):
    try:
        # Ensure the target repository path exists
        if not os.path.exists(repo_path):
            print(f"Error: Repository path '{repo_path}' does not exist.")
            return

        # Iterate over files in the OUTPUT_DIR
        for file_name in os.listdir(OUTPUT_DIR):
            file_path = os.path.join(OUTPUT_DIR, file_name)
            destination_path = os.path.join(repo_path, file_name)

            # If the file is a regular file (not a directory)
            if os.path.isfile(file_path):
                # Check if the file already exists in the destination
                if os.path.exists(destination_path):
                    print(f"Merging {file_name} with the existing file in the repository.")
                    
                    # Read existing and new file content
                    with open(destination_path, "r") as dest_file:
                        existing_content = dest_file.read()
                    
                    with open(file_path, "r") as src_file:
                        new_content = src_file.read()

                    # Merge the content
                    merged_content = merge_files(existing_content, new_content)

                    # Write the merged content back to the destination file
                    with open(destination_path, "w") as dest_file:
                        dest_file.write(merged_content)
                else:
                    # Copy the file directly if it doesn't exist in the repository
                    shutil.copy(file_path, destination_path)
                    print(f"Copied {file_name} to {destination_path}.")
        
        print("All generated files have been copied and merged where necessary.")
    except Exception as e:
        print(f"Error copying files: {e}")


def merge_files(existing_content, new_content):
    """
    Merges two file contents intelligently.
    In this example, it appends new content to the existing content while avoiding duplicates.
    """
    # Split content into lines to compare and merge
    existing_lines = set(existing_content.splitlines())
    new_lines = set(new_content.splitlines())

    # Merge lines, avoiding duplicates
    merged_lines = existing_lines.union(new_lines)

    # Join the merged lines back into a single string
    return "\n".join(sorted(merged_lines))

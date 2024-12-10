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
                if os.path.exists(destination_path):
                    print(f"Merging {file_name} with the existing file in the repository.")

                    # Read existing and new file content
                    with open(destination_path, "r") as dest_file:
                        existing_content = dest_file.read()
                    
                    with open(file_path, "r") as src_file:
                        new_content = src_file.read()

                    # Combine the contents
                    combined_content = merge_terraform_content(existing_content, new_content)

                    # Write the merged content back to the destination file
                    with open(destination_path, "w") as dest_file:
                        dest_file.write(combined_content)

                    print(f"File {file_name} merged successfully.")
                else:
                    # Copy the file directly if it doesn't exist in the repository
                    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                    shutil.copy(file_path, destination_path)
                    print(f"Copied {file_name} to {destination_path}.")
        
        print("All generated files have been copied and merged where necessary.")
    except Exception as e:
        print(f"Error copying files: {e}")


def merge_terraform_content(existing_content, new_content):
    """
    Merges two Terraform files while ensuring structural integrity.
    """
    existing_lines = existing_content.splitlines()
    new_lines = new_content.splitlines()

    # Combine the lines and remove duplicates while preserving order
    combined_lines = list(dict.fromkeys(existing_lines + new_lines))

    # Validate the structure
    combined_content = "\n".join(combined_lines)
    if combined_content.count("{") != combined_content.count("}"):
        print("Warning: Structural issue detected. Fixing unbalanced braces.")
        # Add missing braces if necessary
        combined_content = fix_unbalanced_braces(combined_content)

    return combined_content


def fix_unbalanced_braces(content):
    """
    Ensures Terraform content has balanced braces.
    """
    open_braces = content.count("{")
    close_braces = content.count("}")
    difference = open_braces - close_braces

    if difference > 0:
        # Add missing closing braces at the end
        content += "\n" + "}" * difference
    elif difference < 0:
        # Remove excess closing braces from the end
        for _ in range(abs(difference)):
            if content.strip().endswith("}"):
                content = content.strip()[:-1]

    return content

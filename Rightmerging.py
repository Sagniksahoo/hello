import re

def merge_variables_tf(existing_file_path, new_file_path):
    """Merges variables in `variables.tf` files by avoiding duplicates and preserving structure."""
    try:
        with open(existing_file_path, "r") as existing_file:
            existing_content = existing_file.read()

        with open(new_file_path, "r") as new_file:
            new_content = new_file.read()

        variable_pattern = r'variable\s+"(.*?)"\s*{(.*?)}'
        existing_variables = re.findall(variable_pattern, existing_content, re.DOTALL)
        new_variables = re.findall(variable_pattern, new_content, re.DOTALL)

        # Create a dictionary to hold variables (keyed by variable name)
        variables_dict = {var[0]: var[1].strip() for var in existing_variables}

        # Add or update variables from the new file
        for var_name, var_body in new_variables:
            variables_dict[var_name] = var_body.strip()

        # Reconstruct the merged content
        merged_content = ""
        for var_name, var_body in variables_dict.items():
            merged_content += f'variable "{var_name}" {{\n{var_body}\n}}\n\n'

        # Write back the merged content
        with open(existing_file_path, "w") as merged_file:
            merged_file.write(merged_content)

        print(f"Successfully merged variables in {existing_file_path}.")
    except Exception as e:
        print(f"Error merging variables.tf: {e}")


def merge_generic_tf(existing_file_path, new_file_path):
    """Merges generic `.tf` files line-by-line while avoiding duplicates."""
    try:
        with open(existing_file_path, "r") as existing_file:
            existing_lines = existing_file.readlines()

        with open(new_file_path, "r") as new_file:
            new_lines = new_file.readlines()

        # Merge line-by-line while avoiding duplicates
        unique_lines = list(dict.fromkeys(existing_lines + new_lines))

        with open(existing_file_path, "w") as merged_file:
            merged_file.writelines(unique_lines)

        print(f"Successfully merged {existing_file_path}.")
    except Exception as e:
        print(f"Error merging {existing_file_path}: {e}")


def copy_generated_files(repo_path):
    """Copies generated files to the repository and merges existing files to avoid duplication."""
    try:
        if not os.path.exists(repo_path):
            print(f"Error: Repository path '{repo_path}' does not exist.")
            return

        for file_name in os.listdir(OUTPUT_DIR):
            file_path = os.path.join(OUTPUT_DIR, file_name)
            destination_path = os.path.join(repo_path, file_name)

            if os.path.isfile(file_path):
                if os.path.exists(destination_path):
                    if file_name == "variables.tf":
                        # Merge `variables.tf` specifically
                        merge_variables_tf(destination_path, file_path)
                    elif file_name.endswith(".tf"):
                        # Merge other `.tf` files
                        merge_generic_tf(destination_path, file_path)
                    else:
                        # Merge non-Terraform files as plain text
                        with open(destination_path, "r") as dest_file:
                            existing_content = dest_file.readlines()
                        with open(file_path, "r") as src_file:
                            new_content = src_file.readlines()

                        # Remove duplicates
                        unique_lines = list(dict.fromkeys(existing_content + new_content))

                        with open(destination_path, "w") as dest_file:
                            dest_file.writelines(unique_lines)

                        print(f"Merged non-Terraform file: {file_name}")
                else:
                    # Copy new files directly if they don't exist
                    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                    shutil.copy(file_path, destination_path)
                    print(f"Copied {file_name} to {destination_path}.")

        print("All generated files have been copied and merged where necessary.")
    except Exception as e:
        print(f"Error copying files: {e}")

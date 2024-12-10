import re

def merge_terraform_files(existing_file_path, new_file_path):
    try:
        # Read the content of both files
        with open(existing_file_path, "r") as existing_file:
            existing_content = existing_file.read()

        with open(new_file_path, "r") as new_file:
            new_content = new_file.read()

        # Handle `variables.tf` specifically
        if "variables.tf" in existing_file_path:
            variable_pattern = r'variable\s+"(.*?)"\s*{(.*?)}'
            existing_variables = re.findall(variable_pattern, existing_content, re.DOTALL)
            new_variables = re.findall(variable_pattern, new_content, re.DOTALL)

            # Create a dictionary to store variables (keyed by variable name)
            variables_dict = {var[0]: var[1] for var in existing_variables}

            # Add or update variables from the new content
            for var_name, var_body in new_variables:
                variables_dict[var_name] = var_body.strip()

            # Reconstruct the merged content
            merged_content = ""
            for var_name, var_body in variables_dict.items():
                merged_content += f'variable "{var_name}" {{\n{var_body}\n}}\n\n'

        else:
            # For other Terraform files, merge content line by line to avoid duplicates
            existing_lines = set(existing_content.splitlines())
            new_lines = set(new_content.splitlines())
            merged_lines = sorted(existing_lines | new_lines)

            merged_content = "\n".join(merged_lines)

        # Write the merged content back to the file
        with open(existing_file_path, "w") as merged_file:
            merged_file.write(merged_content)

        print(f"Merged {existing_file_path} successfully.")

    except Exception as e:
        print(f"Error merging Terraform files: {e}")


def copy_generated_files(repo_path):
    try:
        if not os.path.exists(repo_path):
            print(f"Error: Repository path '{repo_path}' does not exist.")
            return

        for file_name in os.listdir(OUTPUT_DIR):
            file_path = os.path.join(OUTPUT_DIR, file_name)
            destination_path = os.path.join(repo_path, file_name)

            if os.path.isfile(file_path):
                if os.path.exists(destination_path):
                    if file_name.endswith(".tf"):
                        print(f"Merging {file_name} with the existing file in the repository.")
                        merge_terraform_files(destination_path, file_path)
                    else:
                        # Merge non-Terraform files (as plain text, removing duplicates)
                        with open(destination_path, "r") as dest_file:
                            existing_content = dest_file.readlines()
                        with open(file_path, "r") as src_file:
                            new_content = src_file.readlines()

                        unique_lines = list(dict.fromkeys(existing_content + new_content))

                        with open(destination_path, "w") as dest_file:
                            dest_file.writelines(unique_lines)

                        print(f"File {file_name} merged successfully.")
                else:
                    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                    shutil.copy(file_path, destination_path)
                    print(f"Copied {file_name} to {destination_path}.")

        print("All generated files have been copied and merged where necessary.")
    except Exception as e:
        print(f"Error copying files: {e}")

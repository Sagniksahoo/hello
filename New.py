import re

def merge_variables_tf(existing_file_path, new_file_path):
    """Merges variables in `variables.tf` while preserving structure and avoiding duplicates."""
    try:
        # Read the existing file
        with open(existing_file_path, "r") as existing_file:
            existing_content = existing_file.read()

        # Read the new file
        with open(new_file_path, "r") as new_file:
            new_content = new_file.read()

        # Regex to match variable blocks, accounting for nested braces
        variable_pattern = r'(variable\s+"(.*?)"\s*{(?:[^{}]*{[^{}]*})*[^{}]*})'
        existing_variables = re.findall(variable_pattern, existing_content, re.DOTALL)
        new_variables = re.findall(variable_pattern, new_content, re.DOTALL)

        # Create a dictionary to hold variables (keyed by variable name)
        variables_dict = {re.search(r'variable\s+"(.*?)"', var[0]).group(1): var[0].strip() for var in existing_variables}

        # Update variables with new values from the new file
        for var_block in new_variables:
            var_name = re.search(r'variable\s+"(.*?)"', var_block[0]).group(1)
            variables_dict[var_name] = var_block[0].strip()

        # Reconstruct the merged content
        merged_content = "\n\n".join(variables_dict.values())

        # Write back the merged content
        with open(existing_file_path, "w") as merged_file:
            merged_file.write(merged_content)

        print(f"Successfully merged variables in {existing_file_path}.")
    except Exception as e:
        print(f"Error merging variables.tf: {e}")

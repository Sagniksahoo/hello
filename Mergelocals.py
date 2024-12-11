import re

def merge_locals_tf(destination_path, new_file_path):
    """
    Merges locals.tf files while preserving structure and avoiding duplicates.
    """
    try:
        # Read the existing and new locals.tf files
        with open(destination_path, "r") as existing_file:
            existing_content = existing_file.read()

        with open(new_file_path, "r") as new_file:
            new_content = new_file.read()

        # Regex to extract key-value pairs from locals blocks
        locals_pattern = r'locals\s*{(.*?)}'
        key_value_pattern = r'(\w+)\s*=\s*(.*?)(?=\n\w+\s*=|\n})'

        # Extract and parse existing and new locals
        existing_locals_match = re.search(locals_pattern, existing_content, re.DOTALL)
        new_locals_match = re.search(locals_pattern, new_content, re.DOTALL)

        existing_locals_body = existing_locals_match.group(1).strip() if existing_locals_match else ""
        new_locals_body = new_locals_match.group(1).strip() if new_locals_match else ""

        # Parse key-value pairs
        existing_key_values = dict(re.findall(key_value_pattern, existing_locals_body, re.DOTALL))
        new_key_values = dict(re.findall(key_value_pattern, new_locals_body, re.DOTALL))

        # Merge key-value pairs, prioritizing new values
        merged_key_values = {**existing_key_values, **new_key_values}

        # Reconstruct the merged locals block
        merged_locals_body = "\n".join([f"  {key} = {value.strip()}" for key, value in merged_key_values.items()])
        merged_content = f"locals {{\n{merged_locals_body}\n}}\n"

        # Write the merged content back to the destination file
        with open(destination_path, "w") as merged_file:
            merged_file.write(merged_content)

        print(f"Successfully merged locals in {destination_path}.")
    except Exception as e:
        print(f"Error merging locals.tf: {e}")

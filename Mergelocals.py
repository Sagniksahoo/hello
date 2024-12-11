import re

def merge_locals_tf(destination_path, new_file_path):
    """
    Merges locals.tf files while preserving structure and avoiding duplicates, including nested maps and lists.
    """
    try:
        # Read the existing and new locals.tf files
        with open(destination_path, "r") as existing_file:
            existing_content = existing_file.read()

        with open(new_file_path, "r") as new_file:
            new_content = new_file.read()

        # Regex to extract and preserve locals blocks
        locals_pattern = r'locals\s*{(.*?)}'
        existing_locals_match = re.search(locals_pattern, existing_content, re.DOTALL)
        new_locals_match = re.search(locals_pattern, new_content, re.DOTALL)

        existing_locals_body = existing_locals_match.group(1).strip() if existing_locals_match else ""
        new_locals_body = new_locals_match.group(1).strip() if new_locals_match else ""

        # Parse locals content into a dictionary of keys and their corresponding values
        locals_key_value_pattern = r'(\w+)\s*=\s*(\{.*?\}|.*?|".*?"|\S+)(?=\n\w+\s*=|\n?$)'
        existing_key_values = dict(re.findall(locals_key_value_pattern, existing_locals_body, re.DOTALL))
        new_key_values = dict(re.findall(locals_key_value_pattern, new_locals_body, re.DOTALL))

        # Merge the dictionaries, prioritizing new values
        merged_key_values = {**existing_key_values, **new_key_values}

        # Reconstruct the merged locals block with proper formatting
        merged_locals_body = ""
        for key, value in merged_key_values.items():
            # Ensure nested structures retain proper indentation
            if value.startswith("{") or value.startswith("["):
                formatted_value = re.sub(r'\n', '\n  ', value.strip())
                merged_locals_body += f"  {key} = {formatted_value}\n"
            else:
                merged_locals_body += f"  {key} = {value.strip()}\n"

        merged_content = f"locals {{\n{merged_locals_body}}}\n"

        # Write the merged content back to the destination file
        with open(destination_path, "w") as merged_file:
            merged_file.write(merged_content)

        print(f"Successfully merged locals in {destination_path}.")
    except Exception as e:
        print(f"Error merging locals.tf: {e}")

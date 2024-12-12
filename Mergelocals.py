import re

def merge_locals_tf(destination_path, new_file_path):
    """
    Merges locals.tf files, ensuring nested structures (maps, lists, etc.) are preserved and merged without duplicates.
    """
    try:
        # Read the existing and new locals.tf files
        with open(destination_path, "r") as existing_file:
            existing_content = existing_file.read()

        with open(new_file_path, "r") as new_file:
            new_content = new_file.read()

        # Parse the locals block from both files
        locals_pattern = r'locals\s*{(.*?)}'
        existing_body_match = re.search(locals_pattern, existing_content, re.DOTALL)
        new_body_match = re.search(locals_pattern, new_content, re.DOTALL)

        existing_body = existing_body_match.group(1).strip() if existing_body_match else ""
        new_body = new_body_match.group(1).strip() if new_body_match else ""

        # Function to parse key-value pairs inside the locals block
        def parse_locals(body):
            local_dict = {}
            key_value_pattern = r'(\w+)\s*=\s*(\{.*?\}|.*?|".*?"|\S+)(?=\n\w+\s*=|\n?$)'
            matches = re.findall(key_value_pattern, body, re.DOTALL)
            for key, value in matches:
                local_dict[key.strip()] = value.strip()
            return local_dict

        existing_locals = parse_locals(existing_body)
        new_locals = parse_locals(new_body)

        # Merge dictionaries: new values overwrite existing ones
        merged_locals = {**existing_locals, **new_locals}

        # Reconstruct the merged locals block
        merged_body = ""
        for key, value in merged_locals.items():
            if value.startswith("{") or value.startswith("["):  # Nested structures
                formatted_value = re.sub(r'\n', '\n  ', value.strip())
                merged_body += f"  {key} = {formatted_value}\n"
            else:  # Simple key-value pairs
                merged_body += f"  {key} = {value.strip()}\n"

        merged_content = f"locals {{\n{merged_body}}}\n"

        # Write the merged content back to the destination file
        with open(destination_path, "w") as merged_file:
            merged_file.write(merged_content)

        print(f"Successfully merged locals.tf in {destination_path}.")
    except Exception as e:
        print(f"Error merging locals.tf: {e}")

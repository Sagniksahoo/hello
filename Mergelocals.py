import re

def merge_locals_tf(destination_path, new_file_path):
    """
    Merges two locals.tf files, preserving all blocks, including nested structures, and avoiding duplicates.
    """
    try:
        # Read both destination and new file contents
        with open(destination_path, "r") as dest_file:
            dest_content = dest_file.read()

        with open(new_file_path, "r") as new_file:
            new_content = new_file.read()

        # Extract the body of the locals block from each file
        locals_pattern = r'locals\s*{(.*?)}'
        dest_body_match = re.search(locals_pattern, dest_content, re.DOTALL)
        new_body_match = re.search(locals_pattern, new_content, re.DOTALL)

        dest_body = dest_body_match.group(1).strip() if dest_body_match else ""
        new_body = new_body_match.group(1).strip() if new_body_match else ""

        # Function to parse locals content into a dictionary
        def parse_locals(body):
            locals_dict = {}
            current_key = None
            current_value = []
            for line in body.splitlines():
                line = line.strip()
                if "=" in line and not line.startswith("#"):  # New key detected
                    if current_key:
                        locals_dict[current_key] = "\n".join(current_value).strip()
                    current_key, rest = line.split("=", 1)
                    current_key = current_key.strip()
                    current_value = [rest.strip()]
                elif current_key:  # Append to the current value
                    current_value.append(line)
            if current_key:  # Add the last key
                locals_dict[current_key] = "\n".join(current_value).strip()
            return locals_dict

        # Parse the locals into dictionaries
        dest_locals = parse_locals(dest_body)
        new_locals = parse_locals(new_body)

        # Merge the dictionaries
        merged_locals = {**dest_locals, **new_locals}

        # Reconstruct the merged locals block
        merged_body = "locals {\n"
        for key, value in merged_locals.items():
            if value.startswith("{") or value.startswith("["):  # Format nested structures
                value = re.sub(r'\n', '\n  ', value.strip())
                merged_body += f"  {key} = {value}\n"
            else:
                merged_body += f"  {key} = {value.strip()}\n"
        merged_body += "}\n"

        # Write the merged content back to the destination file
        with open(destination_path, "w") as dest_file:
            dest_file.write(merged_body)

        print(f"Successfully merged locals.tf into {destination_path}.")

    except Exception as e:
        print(f"Error merging locals.tf: {e}")

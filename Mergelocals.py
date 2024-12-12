import re

def merge_locals_tf(destination_path, new_file_path):
    """
    Merges locals.tf files while handling all fields and avoiding duplicates.
    """
    try:
        # Read the destination and new file contents
        with open(destination_path, "r") as dest_file:
            dest_content = dest_file.read()

        with open(new_file_path, "r") as new_file:
            new_content = new_file.read()

        # Extract locals block content from each file
        locals_pattern = r'locals\s*{(.*?)}'
        dest_body_match = re.search(locals_pattern, dest_content, re.DOTALL)
        new_body_match = re.search(locals_pattern, new_content, re.DOTALL)

        dest_body = dest_body_match.group(1).strip() if dest_body_match else ""
        new_body = new_body_match.group(1).strip() if new_body_match else ""

        # Function to parse locals into a dictionary
        def parse_locals(body):
            locals_dict = {}
            key = None
            value = []
            for line in body.splitlines():
                line = line.strip()
                if "=" in line and not line.startswith("#"):  # New key detected
                    if key:
                        locals_dict[key] = "\n".join(value).strip()
                    key, rest = line.split("=", 1)
                    key = key.strip()
                    value = [rest.strip()]
                elif key:  # Continuation of current key's value
                    value.append(line)
            if key:  # Add the last key
                locals_dict[key] = "\n".join(value).strip()
            return locals_dict

        # Parse the locals content into dictionaries
        dest_locals = parse_locals(dest_body)
        new_locals = parse_locals(new_body)

        # Merge the locals dictionaries
        merged_locals = {**dest_locals, **new_locals}

        # Reconstruct the merged locals block
        merged_body = "locals {\n"
        for key, value in merged_locals.items():
            if value.startswith("{") or value.startswith("["):  # Properly format nested structures
                value = re.sub(r'\n', '\n  ', value.strip())
                merged_body += f"  {key} = {value}\n"
            else:
                merged_body += f"  {key} = {value.strip()}\n"
        merged_body += "}\n"

        # Write back the merged locals block to the destination file
        with open(destination_path, "w") as dest_file:
            dest_file.write(merged_body)

        print(f"Successfully merged locals.tf into {destination_path}.")

    except Exception as e:
        print(f"Error merging locals.tf: {e}")

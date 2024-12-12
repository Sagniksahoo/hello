import re

def merge_locals_tf(destination_path, new_file_path):
    """
    Merges locals.tf files while handling nested maps/lists and preserving formatting.
    """
    try:
        # Read the destination and new file contents
        with open(destination_path, "r") as dest_file:
            dest_content = dest_file.read()

        with open(new_file_path, "r") as new_file:
            new_content = new_file.read()

        # Extract existing and new locals blocks
        locals_pattern = r'locals\s*{(.*?)}'
        dest_body_match = re.search(locals_pattern, dest_content, re.DOTALL)
        new_body_match = re.search(locals_pattern, new_content, re.DOTALL)

        dest_body = dest_body_match.group(1).strip() if dest_body_match else ""
        new_body = new_body_match.group(1).strip() if new_body_match else ""

        # Helper function to parse locals into a dictionary
        def parse_locals(body):
            locals_dict = {}
            current_key = None
            current_value = []

            for line in body.splitlines():
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    if current_key:
                        # Save the previous key-value pair
                        locals_dict[current_key] = "\n".join(current_value).strip()
                    # Start a new key
                    parts = line.split("=", 1)
                    current_key = parts[0].strip()
                    current_value = [parts[1].strip()]
                elif current_key:
                    # Append to the current key's value
                    current_value.append(line)

            if current_key:
                locals_dict[current_key] = "\n".join(current_value).strip()
            return locals_dict

        dest_locals = parse_locals(dest_body)
        new_locals = parse_locals(new_body)

        # Merge locals (new overwrites existing)
        merged_locals = {**dest_locals, **new_locals}

        # Reconstruct the merged locals content
        merged_body = "locals {\n"
        for key, value in merged_locals.items():
            if value.startswith("{") or value.startswith("["):  # Format nested structures
                formatted_value = re.sub(r'\n', '\n  ', value.strip())
                merged_body += f"  {key} = {formatted_value}\n"
            else:
                merged_body += f"  {key} = {value.strip()}\n"
        merged_body += "}\n"

        # Write the merged content back to the destination file
        with open(destination_path, "w") as dest_file:
            dest_file.write(merged_body)

        print(f"Successfully merged locals.tf in {destination_path}.")
    except Exception as e:
        print(f"Error merging locals.tf: {e}")

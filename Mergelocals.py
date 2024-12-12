import re

def merge_locals_tf(destination_path, new_file_path):
    """
    Merges two `locals.tf` files while preserving structure, formatting, and avoiding duplicate keys.
    """
    try:
        # Read both destination and new file contents
        with open(destination_path, "r") as dest_file:
            dest_content = dest_file.read()

        with open(new_file_path, "r") as new_file:
            new_content = new_file.read()

        # Extract content within the locals block
        locals_pattern = r'locals\s*{(.*?)}'
        dest_body_match = re.search(locals_pattern, dest_content, re.DOTALL)
        new_body_match = re.search(locals_pattern, new_content, re.DOTALL)

        dest_body = dest_body_match.group(1).strip() if dest_body_match else ""
        new_body = new_body_match.group(1).strip() if new_body_match else ""

        # Function to parse the locals block into a dictionary of keys and values
        def parse_locals(body):
            locals_dict = {}
            key = None
            value = []
            brace_count = 0

            for line in body.splitlines():
                line = line.strip()

                if "=" in line and brace_count == 0:  # New key starts here
                    if key:
                        locals_dict[key] = "\n".join(value).strip()
                    key, val = map(str.strip, line.split("=", 1))
                    value = [val]
                elif line.startswith("{") or line.startswith("["):  # Start of nested structure
                    value.append(line)
                    brace_count += line.count("{") + line.count("[")
                elif line.endswith("}") or line.endswith("]"):  # End of nested structure
                    value.append(line)
                    brace_count -= line.count("}") + line.count("]")
                elif key:  # Continuation of the current key's value
                    value.append(line)

            if key:  # Add the last key
                locals_dict[key] = "\n".join(value).strip()

            return locals_dict

        # Parse locals content from both files
        dest_locals = parse_locals(dest_body)
        new_locals = parse_locals(new_body)

        # Merge locals: New values overwrite existing ones
        merged_locals = {**dest_locals, **new_locals}

        # Reconstruct the merged content
        merged_body = "locals {\n"
        for key, value in merged_locals.items():
            if value.startswith("{") or value.startswith("["):  # Nested structures
                value = re.sub(r'\n', '\n  ', value.strip())
                merged_body += f"  {key} = {value}\n"
            else:
                merged_body += f"  {key} = {value}\n"
        merged_body += "}\n"

        # Write the merged content back to the destination file
        with open(destination_path, "w") as dest_file:
            dest_file.write(merged_body)

        print(f"Successfully merged locals.tf into {destination_path}.")

    except Exception as e:
        print(f"Error merging locals.tf: {e}")

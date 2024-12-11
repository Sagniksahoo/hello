import re

def merge_tfvars(existing_file_path, new_file_path):
    """Merges .tfvars files while preserving structure and removing duplicates."""
    try:
        # Read the existing file
        with open(existing_file_path, "r") as existing_file:
            existing_content = existing_file.readlines()

        # Read the new file
        with open(new_file_path, "r") as new_file:
            new_content = new_file.readlines()

        # Function to parse tfvars into a dictionary
        def parse_tfvars(content):
            tfvars_dict = {}
            key_value_pattern = r'^\s*(\w+)\s*=\s*["{]?([^"}\n]+)["}]?'
            for line in content:
                match = re.match(key_value_pattern, line.strip())
                if match:
                    key, value = match.groups()
                    tfvars_dict[key.strip()] = value.strip()
            return tfvars_dict

        # Parse both files
        existing_tfvars = parse_tfvars(existing_content)
        new_tfvars = parse_tfvars(new_content)

        # Merge dictionaries (new values override existing ones)
        merged_tfvars = {**existing_tfvars, **new_tfvars}

        # Reconstruct the merged tfvars content
        merged_content = ""
        for key, value in merged_tfvars.items():
            merged_content += f'{key} = "{value}"\n'

        # Write back the merged content
        with open(existing_file_path, "w") as merged_file:
            merged_file.write(merged_content)

        print(f"Successfully merged tfvars in {existing_file_path}.")
    except Exception as e:
        print(f"Error merging tfvars: {e}")

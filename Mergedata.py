import re

def merge_data_tf(destination_path, new_file_path):
    """
    Merges data.tf files while preserving structure and avoiding duplicates.
    """
    try:
        # Read the existing data.tf file
        with open(destination_path, "r") as existing_file:
            existing_content = existing_file.read()

        # Read the new data.tf file
        with open(new_file_path, "r") as new_file:
            new_content = new_file.read()

        # Regex to match data blocks
        data_pattern = r'data\s+"(.*?)"\s+"(.*?)"\s*{(.*?)}'
        existing_data = re.findall(data_pattern, existing_content, re.DOTALL)
        new_data = re.findall(data_pattern, new_content, re.DOTALL)

        # Create a dictionary to hold data blocks (keyed by type and name)
        data_dict = {(data[0], data[1]): data[2].strip() for data in existing_data}

        # Update data blocks with new values from the new file
        for data_type, data_name, data_body in new_data:
            data_dict[(data_type, data_name)] = data_body.strip()

        # Reconstruct the merged content
        merged_content = ""
        for (data_type, data_name), data_body in data_dict.items():
            merged_content += f'data "{data_type}" "{data_name}" {{\n{data_body}\n}}\n\n'

        # Write back the merged content
        with open(destination_path, "w") as merged_file:
            merged_file.write(merged_content)

        print(f"Successfully merged data blocks in {destination_path}.")
    except Exception as e:
        print(f"Error merging data.tf: {e}")

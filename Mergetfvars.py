import hcl2

def merge_tfvars(destination_path, new_file_path):
    """
    Merges tfvars files while preserving the structure and avoiding duplicates, 
    including complex lists and maps.
    """
    try:
        # Read the existing tfvars file
        with open(destination_path, "r") as existing_file:
            existing_content = existing_file.read()

        # Read the new tfvars file
        with open(new_file_path, "r") as new_file:
            new_content = new_file.read()

        # Parse the existing and new tfvars using hcl2
        try:
            existing_data = hcl2.loads(existing_content)
            new_data = hcl2.loads(new_content)
        except Exception as e:
            print(f"Error parsing HCL in one of the tfvars files: {e}")
            return

        # Merge the dictionaries, giving priority to new_data
        merged_data = existing_data.copy()
        for key, value in new_data.items():
            if key in merged_data:
                # Handle merging of lists or maps specifically
                if isinstance(value, list) and isinstance(merged_data[key], list):
                    merged_data[key] = merge_lists(merged_data[key], value)
                elif isinstance(value, dict) and isinstance(merged_data[key], dict):
                    merged_data[key] = {**merged_data[key], **value}
                else:
                    # Overwrite the existing value for other types
                    merged_data[key] = value
            else:
                merged_data[key] = value

        # Write the merged content back to the destination file
        with open(destination_path, "w") as merged_file:
            for key, value in merged_data.items():
                merged_file.write(serialize_tfvars(key, value))

        print(f"Successfully merged tfvars file: {destination_path}")
    except Exception as e:
        print(f"Error merging tfvars file: {e}")

def merge_lists(existing_list, new_list):
    """
    Merges two lists, ensuring no duplicates for simple and complex objects.
    """
    existing_items = {str(item): item for item in existing_list}
    for item in new_list:
        if str(item) not in existing_items:
            existing_items[str(item)] = item
    return list(existing_items.values())

def serialize_tfvars(key, value):
    """
    Serializes key-value pairs into tfvars format.
    """
    if isinstance(value, dict):
        content = f'{key} = {{\n'
        for sub_key, sub_value in value.items():
            content += f'  {sub_key} = {serialize_tfvars_value(sub_value)}\n'
        content += '}\n\n'
    elif isinstance(value, list):
        content = f'{key} = [\n'
        for item in value:
            content += f'  {serialize_tfvars_value(item)},\n'
        content += ']\n\n'
    else:
        content = f'{key} = {serialize_tfvars_value(value)}\n\n'
    return content

def serialize_tfvars_value(value):
    """
    Helper function to serialize individual values for tfvars.
    """
    if isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, dict):
        content = '{\n'
        for sub_key, sub_value in value.items():
            content += f'  {sub_key} = {serialize_tfvars_value(sub_value)}\n'
        content += '}'
        return content
    elif isinstance(value, list):
        return '[ ' + ', '.join(serialize_tfvars_value(item) for item in value) + ' ]'
    else:
        return str(value)

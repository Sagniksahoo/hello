import os
import json
from jinja2 import Template
import shutil

# Paths
TEMPLATE_DIR = "templates"
OUTPUT_DIR = "generated"
VARS_DIR = os.path.join(OUTPUT_DIR, "vars")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(VARS_DIR, exist_ok=True)

# Load JSON requirements
with open("requirements.json") as file:
    data = json.load(file)

# Function to render templates
def render_template(template_path, output_path, context):
    try:
        with open(template_path) as file:
            template = Template(file.read())
        rendered = template.render(context)
        with open(output_path, "w") as output_file:
            output_file.write(rendered)
    except Exception as e:
        print(f"Error generating {output_path}: {e}")

# Map resource types to template files
resource_templates = {
    "app_service_plan": "app_service_plan.tf.j2",
    "app_service": "app_service.tf.j2",
    "function_app": "function_app.tf.j2",
    "key_vault": "key_vault.tf.j2",
    "web_app": "web_app.tf.j2"
}

# Generate Terraform code for all resources in JSON
if "resources" in data and isinstance(data["resources"], list):
    for resource in data["resources"]:
        resource_type = resource.get("type")
        template_file = resource_templates.get(resource_type)
        if template_file:
            output_file = os.path.join(OUTPUT_DIR, f"{resource['name']}.tf")
            render_template(
                os.path.join(TEMPLATE_DIR, template_file),
                output_file,
                resource
            )
            print(f"Generated: {output_file}")
        else:
            print(f"Warning: No template found for resource type '{resource_type}'")
else:
    print("Error: 'resources' key is missing or not a list in JSON.")

# Add the mandatory files
mandatory_files = {
    "main.tf": "templates/main.tf.j2",
    "variables.tf": "templates/variables.tf.j2",
    "outputs.tf": "templates/outputs.tf.j2",
}

for filename, template_path in mandatory_files.items():
    output_file = os.path.join(OUTPUT_DIR, filename)
    render_template(template_path, output_file, data)
    print(f"Generated mandatory file: {output_file}")

# Create vars/ folder and copy .tfvars files
tfvars_files = [
    "dev.tfvars", "prod.tfvars", "staging.tfvars", "common.tfvars"
]

for tfvars_file in tfvars_files:
    output_file = os.path.join(VARS_DIR, tfvars_file)
    # You can customize the content of .tfvars here
    with open(output_file, "w") as file:
        file.write(f"# Variables for {tfvars_file.replace('.tfvars', '')}\n")
        file.write(f"# Add your variables here\n")
    print(f"Generated .tfvars file: {output_file}")

print("Terraform code generation completed with mandatory files and .tfvars.")

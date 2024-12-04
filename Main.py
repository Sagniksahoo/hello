import os
import json
from jinja2 import Template

# Ensure correct paths for the templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the base directory of the script
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")     # Path to templates directory
OUTPUT_DIR = os.path.join(BASE_DIR, "generated")       # Path to output directory
VARS_DIR = os.path.join(OUTPUT_DIR, "vars")            # Path to vars directory

# Ensure output directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(VARS_DIR, exist_ok=True)

# Load the JSON file
with open("requirements.json") as file:
    data = json.load(file)

# Function to render templates
def render_template(template_path, output_path, context):
    try:
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template file not found: {template_path}")
        with open(template_path) as file:
            template = Template(file.read())
        rendered = template.render(context)
        with open(output_path, "w") as output_file:
            output_file.write(rendered)
    except Exception as e:
        print(f"Error generating {output_path}: {e}")

# Function to ask for confirmation before proceeding
def ask_for_confirmation():
    while True:
        # Ask the user for permission to proceed
        user_input = input("Do you want to make changes and deploy? (y/n): ").strip().lower()

        if user_input == 'y':
            print("Proceeding with deployment...")
            return True  # Proceed with the pipeline deployment logic (will be added later)
        elif user_input == 'n':
            print("Deployment canceled.")
            return False  # Stop the deployment process
        else:
            print("Invalid input. Please enter 'y' to proceed or 'n' to cancel.")

# Function to generate Terraform code
def generate_terraform_code(data):
    # Map resource types to template files
    resource_templates = {
        "app_service_plan": "app_service_plan.tf.j2",
        "web_app": "web_app.tf.j2",  # Assuming a template for web app is also needed
        "function_app": "function_app.tf.j2",
        "key_vault": "key_vault.tf.j2"
    }

    # Generate Terraform code for resources
    if "resources" in data and isinstance(data["resources"], list):
        for resource in data["resources"]:
            resource_type = resource.get("type")
            template_file = resource_templates.get(resource_type)
            if template_file:
                template_path = os.path.join(TEMPLATE_DIR, template_file)
                output_file = os.path.join(OUTPUT_DIR, f"{resource['name']}.tf")
                render_template(template_path, output_file, resource)
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
        full_template_path = os.path.join(TEMPLATE_DIR, template_path)
        output_file = os.path.join(OUTPUT_DIR, filename)
        render_template(full_template_path, output_file, data)
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

# Main function
def main():
    # Step 1: Generate the Terraform code (you already have this logic)
    print("Generating Terraform code...")
    generate_terraform_code(data)
    
    # Step 2: Ask for confirmation before deploying
    if ask_for_confirmation():
        # If user confirmed, trigger the pipeline (this part will be added later)
        print("Triggering the pipeline...")
        # Here you will call the pipeline-related function
    else:
        print("Deployment process aborted.")

# Run the main function
if __name__ == "__main__":
    main()

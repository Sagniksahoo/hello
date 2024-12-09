import os
import jinja2

TEMPLATE_DIR = './automation-project/templates'
OUTPUT_DIR = './generated'
VARS_DIR = './generated/tfvars'
MANDATORY_FILES = {
    "main.tf": "./automation-project/templates/main.tf.j2",
    "variables.tf": "./automation-project/templates/variable.tf.j2",
    "resource_group.tf": "./automation-project/templates/resource_group.tf.j2",
    "locals.tf": "./automation-project/templates/locals.tf.j2",
    "data.tf": "./automation-project/templates/data.tf.j2"
}
TFVARS_FILES = {
    "dev-uks.tfvars": "./automation-project/templates/tfvars/dev-uks.tfvars",
    "prod-uks.tfvars": "./automation-project/templates/tfvars/prod-uks.tfvars",
    "stag-uks.tfvars": "./automation-project/templates/tfvars/stag-uks.tfvars",
    "test-uks.tfvars": "./automation-project/templates/tfvars/test-uks.tfvars"
}

resource_templates = {
    "New Azure App Service Plan": "app_service_plan.tf.j2",
    "Azure Windows Web App": "web_app.tf.j2",
    "Azure Linux Function App": "function_app.tf.j2",
    "key_vault": "key_vault.tf.j2",
    "Azure App Insight": "applicationInsights.tf.j2",
    "Azure Log Analytics Workspace": "log_analyticworkspace.tf.j2",
}

# Resource-specific variables
resource_variables = {
    "New Azure App Service Plan": {
        "app_service_plan_name": {
            "type": "string",
            "description": "The name of the Azure App Service Plan"
        },
        "location": {
            "type": "string",
            "description": "The location where the Azure App Service Plan will be created"
        },
        "sku": {
            "type": "string",
            "description": "The SKU of the Azure App Service Plan (e.g., F1, B1, P1v2)"
        }
    },
    # Define variables for other resources here...
}

def render_template(template_path, output_file, data):
    """ Renders the Jinja2 template with the provided data and writes to output_file """
    try:
        with open(template_path, 'r') as template_file:
            template_content = template_file.read()

        template = jinja2.Template(template_content)
        rendered_content = template.render(data=data)

        with open(output_file, 'w') as output:
            output.write(rendered_content)

        print(f"Generated: {output_file}")

    except Exception as e:
        print(f"Error rendering template: {e}")


def generate_terraform_code(data):
    """ Generate Terraform code based on the resources in the provided data """

    # Generate Terraform code for resources
    if "resources" in data and isinstance(data["resources"], list):
        for resource in data["resources"]:
            resource_type = resource.get("name")
            template_file = resource_templates.get(resource_type)

            if template_file:
                template_path = os.path.join(TEMPLATE_DIR, template_file)
                output_file = os.path.join(OUTPUT_DIR, f"{resource['type']}.tf")
                render_template(template_path, output_file, resource)

                # Add variables to variables.tf for the resource
                if resource_type in resource_variables:
                    add_variables_to_tf(resource_type)

            else:
                print(f"Warning: No template found for resource type {resource_type}")

    # Generate mandatory files
    for filename, template_path in MANDATORY_FILES.items():
        output_file = os.path.join(OUTPUT_DIR, filename)
        render_template(template_path, output_file, data)
        print(f"Generated mandatory file: {output_file}")

    # Generate tfvars files
    for filename, template_path in TFVARS_FILES.items():
        output_file = os.path.join(VARS_DIR, filename)
        render_template(template_path, output_file, data)
        print(f"Generated tfvars file: {output_file}")

    print("Terraform code generation completed with mandatory files and .tfvars.")


def add_variables_to_tf(resource_type):
    """ Adds resource-specific variables to the variables.tf file """

    # Check if the resource has associated variables
    if resource_type in resource_variables:
        variables = resource_variables[resource_type]

        # Load the existing variables.tf content
        variables_tf_path = os.path.join(OUTPUT_DIR, "variables.tf")
        if os.path.exists(variables_tf_path):
            with open(variables_tf_path, "r") as file:
                variables_content = file.read()
        else:
            variables_content = ""

        # Use Jinja2 to generate the variables part dynamically
        template = jinja2.Template("""
        {% for var_name, var_details in variables.items() %}
        variable "{{ var_name }}" {
            type        = "{{ var_details['type'] }}"
            description = "{{ var_details['description'] }}"
        }
        {% endfor %}
        """)

        # Render the template with the variables for the resource
        rendered_variables = template.render(variables=variables)

        # Append to the variables.tf file
        variables_content += "\n" + rendered_variables

        # Write the updated content back to variables.tf
        with open(variables_tf_path, "w") as file:
            file.write(variables_content)

        print(f"Updated {variables_tf_path} with variables for {resource_type}.")

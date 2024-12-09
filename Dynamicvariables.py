import jinja2

def add_variables_to_variables_tf(resource_type):
    """ Append resource-specific variables to the variables.tf file """
    
    if resource_type in resource_variables:
        # Get the variables specific to the resource type
        variables = resource_variables[resource_type]
        
        # Path to the variables.tf file
        variables_tf_path = os.path.join(OUTPUT_DIR, "variables.tf")
        
        # Read existing content of variables.tf
        if os.path.exists(variables_tf_path):
            with open(variables_tf_path, "r") as file:
                variables_content = file.read()
        else:
            variables_content = ""
        
        # Define a Jinja2 template for variables
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
    "Azure Windows Web App": {
        "web_app_name": {
            "type": "string",
            "description": "The name of the Azure Windows Web App"
        },
        "app_service_plan_id": {
            "type": "string",
            "description": "The ID of the Azure App Service Plan associated with the Web App"
        },
        "location": {
            "type": "string",
            "description": "The location where the Azure Web App will be deployed"
        }
    },
    # Add other resources here...
}

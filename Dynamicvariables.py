def add_variables_to_variables_tf(resource, data):
    """
    Append resource-specific variables to the variables.tf file, dynamically setting default values from requirements.json.
    """
    variables_path = os.path.join(OUTPUT_DIR, "variables.tf")
    resource_variables = {
        "New Azure App Service Plan": [
            {"name": "app_service_plan_name", "type": "string", "default_key": "ApplicationName"},
            {"name": "app_service_plan_sku", "type": "string", "default_key": "PricingTier"},
            {"name": "worker_count", "type": "number", "default_key": "Workercount"},
            {"name": "max_elastic_worker_count", "type": "number", "default_key": "MaximumElasticWorkerCount"},
            {"name": "zone_balancing", "type": "string", "default_key": "ZoneBalancing"},
        ],
        # Add more resource-specific variable mappings as needed
    }

    resource_type = resource.get("name")
    if resource_type in resource_variables:
        variables_to_add = resource_variables[resource_type]
        parameters = resource.get("parameters", {})
        
        with open(variables_path, "a") as f:
            for variable in variables_to_add:
                # Extract the default value from the parameters if the key exists
                default_value = parameters.get(variable.get("default_key"), "")
                
                # Write variable with the dynamically fetched default value
                f.write(f'variable "{variable["name"]}" {{\n')
                f.write(f'  type = {variable["type"]}\n')
                if default_value:
                    # Add default value if it exists
                    if variable["type"] == "string":
                        f.write(f'  default = "{default_value}"\n')
                    else:  # For non-string types like number
                        f.write(f'  default = {default_value}\n')
                f.write("}\n\n")
        print(f"Updated {variables_path} with variables for {resource_type}.")
    else:
        print(f"No variables defined for resource type: {resource_type}")




def generate_terraform_code(data):
    resource_templates = {
        "New Azure App Service Plan": "app_service_plan.tf.j2",
        "Azure Windows Web App": "web_app.tf.j2",
        # Add more templates here
    }

    # Generate Terraform code for resources
    if "resources" in data and isinstance(data["resources"], list):
        for resource in data["resources"]:
            resource_type = resource.get("name")
            template_file = resource_templates.get(resource_type)
            if template_file:
                template_path = os.path.join(TEMPLATE_DIR, template_file)
                output_file = os.path.join(OUTPUT_DIR, f"{resource['type']}.tf")
                render_template(template_path, output_file, resource)
                print(f"Generated: {output_file}")
                
                # Add variables dynamically to variables.tf
                add_variables_to_variables_tf(resource, data)
            else:
                print(f"Warning: No template found for resource type {resource_type}")

    # Generate mandatory files
    mandatory_files = {
        "main.tf": "./automation-project/templates/main.tf.j2",
        "variables.tf": "./automation-project/templates/variables.tf.j2",
        "resource_group.tf": "./automation-project/templates/resource_group.tf.j2",
        "locals.tf": "./automation-project/templates/locals.tf.j2",
        "data.tf": "./automation-project/templates/data.tf.j2",
    }

    for filename, template_path in mandatory_files.items():
        output_file = os.path.join(OUTPUT_DIR, filename)
        render_template(template_path, output_file, data)
        print(f"Generated mandatory file: {output_file}")

    # Generate tfvars files
    tfvars_files = {
        "dev-uks.tfvars": "./automation-project/templates/tfvars/dev-uks.tfvars.j2",
        "prod-uks.tfvars": "./automation-project/templates/tfvars/prod-uks.tfvars.j2",
        "stag-uks.tfvars": "./automation-project/templates/tfvars/stag-uks.tfvars.j2",
        "test-uks.tfvars": "./automation-project/templates/tfvars/test-uks.tfvars.j2",
    }

    for filename, template_path in tfvars_files.items():
        output_file = os.path.join(VARS_DIR, filename)
        render_template(template_path, output_file, data)
        print(f"Generated tfvars file: {output_file}")

    print("Terraform code generation completed with mandatory files and .tfvars.")






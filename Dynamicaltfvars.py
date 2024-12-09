def generate_tfvars(data):
    """
    Generate .tfvars files with dynamically added values from requirements.json.
    """
    tfvars_files = {
        "dev-uks.tfvars": "./automation-project/templates/tfvars/dev-uks.tfvars.j2",
        "prod-uks.tfvars": "./automation-project/templates/tfvars/prod-uks.tfvars.j2",
        "stag-uks.tfvars": "./automation-project/templates/tfvars/stag-uks.tfvars.j2",
        "test-uks.tfvars": "./automation-project/templates/tfvars/test-uks.tfvars.j2",
    }

    # List of variables to include dynamically
    dynamic_variables = {
        "New Azure App Service Plan": [
            {"name": "app_service_plan_sku", "key": "PricingTier"},
            {"name": "worker_count", "key": "Workercount"},
            {"name": "max_elastic_worker_count", "key": "MaximumElasticWorkerCount"},
            {"name": "zone_balancing", "key": "ZoneBalancing"},
        ],
        # Add more resource-specific mappings here if needed
    }

    for tfvars_file, template_path in tfvars_files.items():
        output_file = os.path.join(VARS_DIR, tfvars_file)

        # Start with existing template content
        content = ""
        if os.path.exists(template_path):
            with open(template_path, "r") as template:
                content = template.read()

        # Append dynamic variables based on resources
        for resource in data.get("resources", []):
            resource_type = resource.get("name")
            resource_parameters = resource.get("parameters", {})
            if resource_type in dynamic_variables:
                variables = dynamic_variables[resource_type]
                for variable in variables:
                    key = variable.get("key")
                    value = resource_parameters.get(key)
                    if value is not None:
                        # Append the variable to tfvars content
                        if isinstance(value, str):
                            content += f'\n{variable["name"]} = "{value}"'
                        else:
                            content += f'\n{variable["name"]} = {value}'

        # Write the final tfvars file
        with open(output_file, "w") as tfvars_file:
            tfvars_file.write(content)
        print(f"Generated tfvars file with dynamic values: {output_file}")


#!/bin/bash

# GitHub variables
echo "Select the organization:"
select Organisation in "Asda-ETS-Infra" "Another-Organization"; do
    if [[ -n $Organisation ]]; then
        echo "You selected $Organisation"
        break
    else
        echo "Invalid selection. Please try again."
    fi
done

# Prompt for the new repository name
read -p "Enter the new repository name: " NewRepoName
GitHubRepoName="$Organisation/$NewRepoName"
TeamSlug='ets-eng-infra-code-reviewers'

# Display the entered values
echo "New Repository Name: $NewRepoName"
echo "GitHub Repository: $GitHubRepoName"

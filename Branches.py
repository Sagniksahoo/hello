def handle_github_operations():
    user_choice = input("Do you want to create a new GitHub repository? (y/n): ").strip().lower()

    if user_choice == "y":
        print("Creating a new GitHub repository...")
        run_git_pipeline()
    elif user_choice == "n":
        print(f"Fetching repositories for organization {ORGANIZATION_NAME}...")
        repos = fetch_organization_repositories()

        if not repos:
            print(f"No repositories found for organization '{ORGANIZATION_NAME}'. Exiting...")
            return

        print("Available repositories:")
        for i, repo_name in enumerate(repos, start=1):
            print(f"{i}. {repo_name}")

        selected_repo_index = int(input("Select a repository by number: ")) - 1
        selected_repo = repos[selected_repo_index]
        print(f"Selected repository: {selected_repo}")

        repo_path = clone_repository(selected_repo)
        if repo_path:
            manage_branches(repo_path)
            copy_generated_files(repo_path)
            print("Changes are ready to be committed and pushed.")
        else:
            print("Failed to clone the repository.")
    else:
        print("Invalid input. Exiting...")

def list_branches(repo_path):
    try:
        # Get the list of branches
        result = subprocess.run(
            ["git", "branch", "-r"],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            text=True,
            check=True
        )
        branches = result.stdout.strip().split("\n")
        return [branch.split("/")[-1] for branch in branches if "->" not in branch]
    except subprocess.CalledProcessError as e:
        print(f"Error listing branches: {e}")
        return []

def manage_branches(repo_path):
    print("Fetching available branches...")
    branches = list_branches(repo_path)

    if not branches:
        print("No branches available. Exiting...")
        return

    user_choice = input("Do you want to create a new branch? (y/n): ").strip().lower()

    if user_choice == "y":
        print("Available branches:")
        for i, branch in enumerate(branches, start=1):
            print(f"{i}. {branch}")

        selected_branch_index = int(input("Select a base branch by number: ")) - 1
        base_branch = branches[selected_branch_index]
        print(f"Selected base branch: {base_branch}")

        new_branch = input("Enter the name of the new branch: ").strip()

        try:
            # Checkout the base branch and create a new branch
            subprocess.run(["git", "checkout", base_branch], cwd=repo_path, check=True)
            subprocess.run(["git", "checkout", "-b", new_branch], cwd=repo_path, check=True)
            print(f"Created and switched to new branch: {new_branch}")
        except subprocess.CalledProcessError as e:
            print(f"Error creating new branch: {e}")
    elif user_choice == "n":
        print("Available branches:")
        for i, branch in enumerate(branches, start=1):
            print(f"{i}. {branch}")

        selected_branch_index = int(input("Select a branch by number: ")) - 1
        selected_branch = branches[selected_branch_index]
        print(f"Selected branch: {selected_branch}")

        try:
            # Checkout the selected branch
            subprocess.run(["git", "checkout", selected_branch], cwd=repo_path, check=True)
            print(f"Switched to branch: {selected_branch}")
        except subprocess.CalledProcessError as e:
            print(f"Error switching branches: {e}")
    else:
        print("Invalid input. Exiting...")

def list_branches(repo_path):
    try:
        # Get the list of branches, including their remote names
        result = subprocess.run(
            ["git", "branch", "-r"],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            text=True,
            check=True
        )
        branches = result.stdout.strip().split("\n")
        # Remove 'origin/' prefix for display purposes
        return [branch.strip() for branch in branches if branch.strip()]
    except subprocess.CalledProcessError as e:
        print(f"Error listing branches: {e}")
        return []



def manage_branches(repo_path):
    print("Fetching available branches...")

    # Fetch all branches from the remote
    try:
        subprocess.run(["git", "fetch", "--all"], cwd=repo_path, check=True)
        print("Fetched all branches.")
    except subprocess.CalledProcessError as e:
        print(f"Error fetching branches: {e}")
        return

    # List all remote branches
    branches = list_branches(repo_path)

    if not branches:
        print("No branches available. Exiting...")
        return

    print("Available branches:")
    for i, branch in enumerate(branches, start=1):
        print(f"{i}. {branch}")

    user_choice = input("Do you want to create a new branch? (y/n): ").strip().lower()

    if user_choice == "y":
        selected_branch_index = int(input("Select a base branch by number: ")) - 1
        base_branch = branches[selected_branch_index].strip()
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
        selected_branch_index = int(input("Select a branch by number: ")) - 1
        selected_branch = branches[selected_branch_index].strip()
        print(f"Selected branch: {selected_branch}")

        try:
            # Checkout the selected branch
            subprocess.run(["git", "checkout", selected_branch], cwd=repo_path, check=True)
            print(f"Switched to branch: {selected_branch}")
        except subprocess.CalledProcessError as e:
            print(f"Error switching branches: {e}")
    else:
        print("Invalid input. Exiting...")

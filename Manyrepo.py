import os
import subprocess
import requests

def get_repositories(org_name, token):
    """Fetch all repositories in a GitHub organization."""
    base_url = f"https://api.github.com/orgs/{org_name}/repos"
    headers = {"Authorization": f"token {token}"}
    all_repos = []
    page = 1

    while True:
        response = requests.get(base_url, headers=headers, params={"page": page, "per_page": 100})
        if response.status_code != 200:
            print(f"Error fetching repositories: {response.status_code} {response.text}")
            return []

        repos = response.json()
        if not repos:  # Break if no more repositories are returned
            break

        all_repos.extend(repos)
        page += 1

    return [repo['name'] for repo in all_repos]

def select_repository_and_branch(org_name, token):
    """Fetch repositories, allow the user to select one, and then select or create a branch."""
    print("Fetching repositories...")
    repos = get_repositories(org_name, token)

    if not repos:
        print("No repositories found or an error occurred.")
        return None, None

    print("\nRepositories in the organization:")
    for i, repo in enumerate(repos, start=1):
        print(f"{i}. {repo}")

    repo_index = int(input("\nSelect a repository by number: ")) - 1
    if 0 <= repo_index < len(repos):
        selected_repo = repos[repo_index]
        print(f"Selected repository: {selected_repo}")
    else:
        print("Invalid selection.")
        return None, None

    # Clone the selected repository
    clone_path = os.path.join("generated", selected_repo)
    os.makedirs(clone_path, exist_ok=True)

    repo_url = f"https://github.com/{org_name}/{selected_repo}.git"
    try:
        print(f"Cloning repository {selected_repo} into {clone_path}...")
        subprocess.run(["git", "clone", repo_url, clone_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        return None, None

    # Fetch and manage branches
    os.chdir(clone_path)
    subprocess.run(["git", "fetch", "--all"], check=True)

    branches = subprocess.check_output(["git", "branch", "-r"]).decode("utf-8").strip().split("\n")
    branches = [b.strip().replace("origin/", "") for b in branches if "HEAD" not in b]

    print("\nAvailable branches:")
    for i, branch in enumerate(branches, start=1):
        print(f"{i}. {branch}")

    create_new_branch = input("\nDo you want to create a new branch? (y/n): ").strip().lower()
    if create_new_branch == "y":
        base_branch_index = int(input("\nSelect a base branch by number: ")) - 1
        if 0 <= base_branch_index < len(branches):
            base_branch = branches[base_branch_index]
            print(f"Selected base branch: {base_branch}")
            subprocess.run(["git", "checkout", base_branch], check=True)

            new_branch_name = input("Enter the name of the new branch: ").strip()
            try:
                subprocess.run(["git", "checkout", "-b", new_branch_name], check=True)
                print(f"New branch '{new_branch_name}' created based on '{base_branch}'.")
            except subprocess.CalledProcessError as e:
                print(f"Error creating new branch: {e}")
                return None, None
        else:
            print("Invalid base branch selection.")
            return None, None
    else:
        branch_index = int(input("\nSelect a branch by number: ")) - 1
        if 0 <= branch_index < len(branches):
            selected_branch = branches[branch_index]
            try:
                subprocess.run(["git", "checkout", selected_branch], check=True)
                print(f"Switched to branch '{selected_branch}'.")
            except subprocess.CalledProcessError as e:
                print(f"Error switching branches: {e}")
                return None, None
        else:
            print("Invalid branch selection.")
            return None, None

    os.chdir("../../")  # Move back to the main directory
    return selected_repo, clone_path

def main():
    org_name = input("Enter your GitHub organization name: ").strip()
    token = input("Enter your GitHub personal access token: ").strip()

    selected_repo, clone_path = select_repository_and_branch(org_name, token)
    if selected_repo and clone_path:
        # Copy files to the repository folder
        try:
            for root, dirs, files in os.walk("generated"):
                for file in files:
                    src_file = os.path.join(root, file)
                    dest_file = os.path.join(clone_path, os.path.relpath(src_file, "generated"))
                    os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                    subprocess.run(["cp", src_file, dest_file], check=True)
            print("Generated files copied successfully.")
        except Exception as e:
            print(f"Error copying files: {e}")

        print(f"Changes are ready to be committed in {clone_path}.")
    else:
        print("No repository or branch selected. Exiting.")

if __name__ == "__main__":
    main()

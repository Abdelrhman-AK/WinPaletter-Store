import os
import sys
from datetime import datetime
from git import Repo
import hashlib

# Function to set the action output for GitHub Actions workflow
def set_action_output(name: str, value: str):
    # Open the GITHUB_OUTPUT file and append the output in the required format
    with open(os.environ["GITHUB_OUTPUT"], "a") as output_file:
        output_file.write(f"{name}={value}\n")

# Function to calculate the MD5 hash of a given file
def calc_md5(file_path: str) -> str:
    try:
        # Check if the file exists before trying to read
        if os.path.exists(file_path):
            md5_hash = hashlib.md5()
            # Open file in binary mode and read it in chunks
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    md5_hash.update(byte_block)
            return md5_hash.hexdigest().upper()  # Return the MD5 hash as uppercase
    except Exception:
        # In case of any error, return '0' to indicate failure
        return '0'
    # Default return in case file does not exist
    return '0'

def main():
    # Get input parameters from command line arguments
    path = sys.argv[1]  # Directory path to search for files
    extension = '.wpth'  # File extension to filter
    outputfile = sys.argv[2]  # Output file where results will be saved

    # Get GitHub repository owner, repository name and commiter from the environment variable
    repository_info = os.getenv("GITHUB_REPOSITORY")
    owner, repo_name = repository_info.split("/")
    committer = os.getenv("GITHUB_ACTOR", "Unknown")  # Defaults to 'Unknown' if not available

    # Initialize the git repository object (get current repository)
    repo = Repo('.', search_parent_directories=True)

    print(f'Searching inside directory: {path} for files with extension: {extension}')

    path_count = 0  # Initialize counter for the number of files found
    paths = []  # List to hold details of the files

    # Walk through the directory to find files with the specified extension
    for root, dirs, files in os.walk(path):
        for file in files:
            # Only process files with the specified extension
            if file.endswith(extension):
                targetfile = os.path.join(root, file)  # Full path of the .wpth file
                targetpack = os.path.join(root, file.replace(extension, '.wptp'))  # Full path of the corresponding .wptp file
                
                # Calculate MD5 hashes for both the .wpth and .wptp files
                md5_file = calc_md5(targetfile)
                md5_pack = calc_md5(targetpack) if os.path.exists(targetpack) else '0'  # If .wptp file exists, calculate its MD5, else return '0'

                # GitHub raw URL for the .wpth file
                url_file = f'https://github.com/{owner}/{repo_name}/blob/main/{targetfile}?raw=true'
                # GitHub raw URL for the .wptp file (if exists)
                url_pack = f'https://github.com/{owner}/{repo_name}/blob/main/{targetpack}?raw=true' if os.path.exists(targetpack) else ''

                # Build a string with the required information: MD5 hashes and URLs
                path_info = f"{md5_file}|{md5_pack}|{url_file}"
                if url_pack:  # Add the .wptp URL if it exists
                    path_info += f'|{url_pack}'

                # Append the file information to the paths list
                paths.append(path_info)
                path_count += 1  # Increment the file count

    # Set GitHub Actions output for path count and paths as a single string
    set_action_output('path_count', path_count)
    set_action_output('paths', ' '.join(paths))  # Join file paths into a single string for output

    # Print the results for the user
    print(f'Found {path_count} files:')
    print('\n'.join(paths))  # Print each file's details

    # Write the paths data to the output file
    with open(outputfile, 'w') as f:
        f.write('\n'.join(paths))  # Join file paths with newlines before writing

    # Add the output file to the git index (staging area)
    repo.index.add([outputfile])
    # Commit the changes with a timestamp
    repo.index.commit(f'{committer} has modified the themes database on {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}, provided that GMT is 00:00')
    # Push the commit to the remote repository
    repo.remotes[0].push()

    # Exit the program successfully
    sys.exit(0)

# If this script is executed directly, run the main function
if __name__ == "__main__":
    main()

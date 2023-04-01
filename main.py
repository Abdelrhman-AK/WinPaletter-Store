import os
import sys
from datetime import datetime
from git.repo import Repo
import git
    
def set_action_output(name: str, value: str):
    with open(os.environ["GITHUB_OUTPUT"], "a") as myfile:
        myfile.write(f"{name}={value}\n")

def main():
    path = sys.argv[1]
    extension = sys.argv[2]
    outputfile = sys.argv[3]
    repo = git.Repo('.', search_parent_directories=True)
    repo.working_tree_dir
    
    print('Searching inside directory: ' + path)
    print('for files with extention: ' + extension)

    path_count = 0
    paths = ''
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(f'{extension}'):
                paths = paths + root + '/' + str(file) + ' '
                path_count = path_count + 1

    set_action_output('path_count', path_count)
    set_action_output('paths', paths)
    print('The following are found: ')
    print(paths)

    f = open("" + outputfile + "", "w")
    f.write(paths)
    f.close()

    repo.index.add(['' + outputfile + ''])
    repo.index.commit('Themes database is modified ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    origin = repo.remotes[0]
    origin.push()

    sys.exit(0)


if __name__ == "__main__":
    main()

import os
import sys


def set_action_output(name: str, value: str):
    with open(os.environ["GITHUB_OUTPUT"], "a") as myfile:
        myfile.write(f"{name}={value}\n")

def main():
    set_action_output('Hello', 'Hello')
    print('Hello')

    sys.exit(0)
if __name__ == "__main__":
    main()

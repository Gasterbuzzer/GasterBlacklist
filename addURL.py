"""
Python Bat to add new blocklist Urls.
"""

# Imports
from datetime import datetime
import fileinput
import subprocess
import re
import shutil


def main() -> None:
    """
    Main function
    """

    print("Running console... (Use 'q' or 'quit' to exit) ('h' or 'help' for all commands)\n")

    # Pull current changes to make sure that we don't make any unchanged changes.
    pull_git()

    # Interactive Loop
    active = True

    while active:

        print("CMD: ", end="")
        user_input = input()

        match user_input:  # Matches quick commands, if not in list, passes it go complex commands
            case "q":
                active = False
                break

            case "quit":
                active = False
                break

            case "h":
                help_print()

            case "help":
                help_print()

            case "push":
                upload_changes()

            case "pull":
                pull_git()

            case _:
                complex_command_handling(user_input)


def complex_command_handling(command: str) -> None:
    """
    Handles complex commands requiring parameters
    """

    if command[:3] == "add":
        # Test URL: tracking.india.miui.com
        add_url(command[4:])
    elif command[:4] == "find":
        find_url(command[5:])
    elif command[:6] == "remove":
        remove_url(command[7:])
    else:
        print(f"Unknown command '{command}'. ('h' or 'help' for all commands)\n")


def contains_http(url: str) -> bool:
    """
    Checks if string contains http returns true if true
    """

    contains = False

    if "http" in url:
        contains = True
    elif "https" in url:
        contains = True
    elif "http://" in url:
        contains = True
    elif "https://" in url:
        contains = True

    return contains


def find_url(url: str) -> None:
    """
    Prints if url in a list.
    """

    file_name = "hosts"
    found = False

    if contains_http(url):
        print("ERROR: url contains 'http/s' and is not valid.\n")
        return

    # If it includes "0.0.0.0"
    if "0.0.0.0" in url[:8]:
        url = url[8:]

    url_to_find = "0.0.0.0 " + url + "\n"

    for line in fileinput.input(files=file_name, inplace=True):
        print(f'{line}', end='')

        if line == url_to_find:
            # Found URL
            found = True

    url_to_find = "0.0.0.0 " + url

    if found:
        print(f"\nFound URL: '{url_to_find}' in {file_name}.\n")
    else:
        print(f"\n'{url_to_find}' is not in {file_name}.\n")


def add_url(url: str) -> None:
    """
    Add url to a host list
    """

    file_name = "hosts"
    file_name_txt_version = "hosts.txt"

    if contains_http(url):
        print("ERROR: url contains 'http/s' and is not valid.\n")
        return

    with open(file_name) as f:
        text = f.read()

        # Checks if url already in file.
        if url in text:
            print(f"Error: URL '{url}' already in list. \n")
            return

    # For txt version:
    with open(file_name_txt_version) as f:
        text_txt_version = f.read()

    # If not, then we get our current day.
    day_string = datetime.today().strftime('%d.%m.%Y')  # %Y-%m-%d
    # day_string = "3" + day_string[1:] # Test if you want to see if the day gets added.

    if day_string not in text:
        # Create day comment
        print(f"Day String not Found: {day_string}, creating one...")

        for line in fileinput.input(files=file_name, inplace=True):
            if "# END of Blacklist" in line:
                # Adding Day String
                print(f"\n# {day_string}\n")

            print(f'{line}', end='')

    for line in fileinput.input(files=file_name, inplace=True):
        print(f'{line}', end='')

        if f"# {day_string}" in line:
            # Adding URL
            print(f"0.0.0.0 {url}")

    # Now for txt version:
    if day_string not in text_txt_version:

        for line in fileinput.input(files=file_name_txt_version, inplace=True):
            if "# END of Blacklist" in line:
                # Adding Day String
                print(f"\n# {day_string}\n")

            print(f'{line}', end='')

    for line in fileinput.input(files=file_name_txt_version, inplace=True):
        print(f'{line}', end='')

        if f"# {day_string}" in line:
            # Adding URL
            print(f"{url}")

    print(f"\nAdded URL: {url} to {file_name} at section {day_string}.\n")


def remove_url(url: str) -> None:
    """
    Remove url to a host list
    """

    file_name = "hosts"
    file_name_txt_version = "hosts"

    found = False

    escaped_search_string = re.escape(url)
    pattern = r"\b" + escaped_search_string + r"\b"

    if contains_http(url):
        print("ERROR: url contains 'http/s' and is not valid.\n")
        return

    # First checks if in list
    with open(file_name) as f:
        text = f.read()

        # Checks if url already in file.

        # Updated to check for exact match and nothing else.
        if bool(re.search(pattern, text)):
            found = True

    # Txt Version
    with open(file_name_txt_version) as f:
        text_txt_version = f.read()

    if not found:
        print("\nERROR: Did not find the url to remove.\n")
        return

    for line in fileinput.input(files=file_name, inplace=True):

        # Edited to now check for the exact string and not something that could be it.
        if not bool(re.search(pattern, line)):
            print(f'{line}', end='')

    # For TXT now:
    for line in fileinput.input(files=file_name_txt_version, inplace=True):

        # Edited to now check for the exact string and not something that could be it.
        if not bool(re.search(pattern, line)):
            print(f'{line}', end='')

    print(f"\nRemoved URL: {url} from {file_name}\n")


def help_print() -> None:
    """
    Prints all commands to console
    """

    print("\nAll commands: ")
    print("\t\t'h' or 'help' : Shows all commands (currently)")
    print("\t\t'q' or 'quit' : Quit the program")
    print("\t\t'add %url%'   : Adds url to list (%url% should be a valid url without http or https.)")
    print("\t\t'find %url%'  : Checks if url in list (%url% should be a valid url without http or https.)")
    print("\t\t'remove %url%': Remove url from list (%url% should be a valid url without http or https.)")
    print("\t\t'push'        : Pushes changes made to github/repository.")
    print("\t\t'pull'        : Pulls changes made to github/repository.")

    print("\n")


def pull_git() -> None:
    """
    Pulls git to get the newest changes.
    """

    # Run "git pull" at current location.
    process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
    output = process.communicate()[0]

    print(f"\nDebug: Git Pull Status: '{output}'.")


def commit_changes_git() -> None:
    """
    Commits current changes to git.
    """

    # Run "git add ." at the current location.
    process = subprocess.Popen(["git", "add", "."], stdout=subprocess.PIPE)
    output = process.communicate()[0]

    print(f"\nDebug: Git Adds all files not in .gitignore: '{output}'.")

    # Run "git commit -m 'current date'" at the current location.

    # Get the current date as a commit message
    day_string = datetime.today().strftime('%d.%m.%Y')  # %Y-%m-%d

    process = subprocess.Popen(["git", "commit", "-m", day_string], stdout=subprocess.PIPE)
    output = process.communicate()[0]

    print(f"\nDebug: Commits the changes with current day as commit message: '{output}'.\n")


def push_changes_git() -> None:
    """
    Pushes current changes to git.
    """

    # Run "git push" at the current location.
    process = subprocess.Popen(["git", "push"], stdout=subprocess.PIPE)
    output = process.communicate()[0]

    print(f"\nDebug: Pushed changes with git: '{output}'.\n")


def upload_changes() -> None:
    """
    Commits and Pushes current changes.
    """

    commit_changes_git()
    push_changes_git()


if __name__ == "__main__":
    main()

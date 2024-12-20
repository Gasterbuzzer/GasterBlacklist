"""
Small package for displaying and processing commands.
"""
import fileinput
# Imports
from datetime import datetime
import re

from GasterBlacklistUrlAdderPackage.gitHelper import GitHelper

def main() -> None:
    """
    Main function
    """

    print("\nRunning console... (Use 'q', 'quit' or 'exit' to exit) ('h' or 'help' for all commands)")

    # Pull current changes to make sure that we don't make any unchanged changes. Also checks if git is installed.
    GitHelper.pull_git()

    while True:
        print("CMD: ", end="")

        complex_command_handling(input())

def complex_command_handling(command: str) -> None:
    """
    Handles complex commands requiring parameters
    """

    # Split commands
    command_parts = command.split()

    # Add a new url to list
    if command_parts[0].lower() == "add" and len(command_parts) == 2:
        add_url(command_parts[1])

    # Check if an url exists
    elif command_parts[0].lower() == "find" and len(command_parts) >= 2:
        find_url(''.join(command_parts[1:]))

    # Remove url from list
    elif command_parts[0].lower() == "remove" and len(command_parts) == 2:
        remove_url(command_parts[1])

    # Pull git
    elif command_parts[0].lower() == "pull" and len(command_parts) == 1:
        GitHelper.pull_git()

    # Push git
    elif command_parts[0].lower() == "push" and len(command_parts) == 1:
        GitHelper.push_changes_git()

    # Help command
    elif command_parts[0].lower() in ["h", "help"] and len(command_parts) == 1:
        help_print()

    # Quit
    elif command_parts[0].lower() in ["q", "quit", "exit"] and len(command_parts) == 1:
        exit(0)

    # Unknown command
    else:
        print(f"Unknown command '{command}' of length {len(command_parts)}. ('h' or 'help' for all commands)\n")


def contains_http(url: str) -> bool:
    """
    Checks if string contains http returns true if true
    :param url: Url to check if contains http
    :return: True if contains http or any prefix of that similar matter
    """

    return url.startswith("http")

def remove_http(url: str) -> str:
    """
    Removes http part from the url.
    :param url: Url to change
    :return: Url without front part.
    """

    url_front_part = url[:8].replace("http://", "").replace("https://", "").replace("http", "").replace("http", "")
    url_back_part = url[8:]

    return url_front_part + url_back_part


def find_url(url: str) -> bool:
    """
    Prints if url in a list.
    :param url: Url to find in file.
    :return: True if url in list.
    """

    # We only need to search in one file, not both
    FILE_NAME = "hosts"

    if contains_http(url):
        print("WARNING: Given URL starts with 'http/s' or similar and is thus not valid. Attempted removal:\n")
        url = remove_http(url)
        print(f"{url}\n")

    # If it includes "0.0.0.0" we remove it from the beginning
    if "0.0.0.0" in url[:8]:
        print("WARNING: Given url started with '0.0.0.0', attempting to remove it:")
        url = url.replace("0.0.0.0", "")
        print(f"'{url}'\n")

    url_to_find = "0.0.0.0 " + url + "\n"

    with open(FILE_NAME, "r") as file:
        # Move to the end of the file
        file.seek(0, 2)

        # Start reading backwards
        buffer = []
        position = file.tell()

        while position > 0:
            position -= 1
            file.seek(position)
            char = file.read(1)

            if char == '\n' and buffer:
                # If a newline is encountered, return true
                if url_to_find == ''.join(reversed(buffer)):
                    print(f"\nFound URL: '{url_to_find.replace("\n", "")}' in {FILE_NAME}.\n")
                    return True
                buffer = []
            else:
                buffer.append(char)

        # Yield the last line if the file doesn't end with a newline
        if buffer and url_to_find == ''.join(reversed(buffer)):
            print(f"\nFound URL: '{url_to_find.replace("\n", "")}' in {FILE_NAME}.\n")
            return True

    # Not found, we finish
    print(f"\n'{url_to_find.replace("\n", "")}' is not in {FILE_NAME}.\n")
    return False

def add_url(url: str) -> None:
    """
    Add the given url to both host lists
    :param url: Url to add to the list
    """

    FILE_NAME = "hosts"
    FILE_NAME_TXT_VERSION = "hosts.txt"

    if contains_http(url):
        print("WARNING: Given URL starts with 'http/s' or similar and is thus not valid. Attempted removal:\n")
        url = remove_http(url)
        print(f"'{url}'\n")

    # If it includes "0.0.0.0" we remove it from the beginning
    if "0.0.0.0" in url[:8]:
        print("WARNING: Given url started with '0.0.0.0', attempting to remove it:")
        url = url.replace("0.0.0.0", "")
        print(f"{url}\n")

    if find_url(url):
        print(f"ERROR: URL '{url}' already in list. \n")
        return

    # Get the day string, needed to check if a section needs it.
    day_string = datetime.today().strftime('%d.%m.%Y')  # %Y-%m-%d
    write_position_normal = -1
    write_position_txt = -1

    all_lines_host_normal = [] # Initialize list empty
    all_lines_host_txt = [] # Initialize list empty

    with open(FILE_NAME, "r") as file:

        all_lines_host_normal = file.readlines()

        # We read backwards since its more likely to find the day string at end rather than earlier
        line_index = len(all_lines_host_normal) - 1
        while True:

            if line_index <= 0 or line_index >= len(all_lines_host_normal):
                break

            if f"# {day_string}\n" == all_lines_host_normal[line_index]:
                print(f"\nFound day string in file at {line_index}.\n")

                # Find end of section or end of blacklist
                while True:
                    line_index += 1 # Go forward
                    if "# END of Blacklist" in all_lines_host_normal[line_index] or (all_lines_host_normal[line_index] in ["", "\n", " "]): # End of blacklist or end of section
                        while True:
                            line_index -= 1 # Go back until we find something
                            if all_lines_host_normal[line_index] not in ["", "\n", " "]:
                                line_index += 1 # We found the position
                                write_position_normal = line_index
                                break # We break the third while loop
                        break # We break the second while loop
                break # We break from the first while loop since we are done

            line_index -= 1 # We didn't find the day string

    with open(FILE_NAME_TXT_VERSION, "r") as file: # Get host file contents for txt type
        all_lines_host_txt = file.readlines()

        # We read backwards since its more likely to find the day string at end rather than earlier
        line_index = len(all_lines_host_txt) - 1
        while True:

            if line_index <= 0 or line_index >= len(all_lines_host_txt):
                break

            if f"# {day_string}\n" == all_lines_host_txt[line_index]:
                # Find end of section or end of blacklist, which is different for this file.
                while True:
                    line_index += 1  # Go forward
                    if "# END of Blacklist" in all_lines_host_txt[line_index] or (
                            all_lines_host_txt[line_index] in ["", "\n", " "]):  # End of blacklist or end of section
                        while True:
                            line_index -= 1  # Go back until we find something
                            if all_lines_host_txt[line_index] not in ["", "\n", " "]:
                                line_index += 1  # We found the position
                                write_position_txt = line_index
                                break  # We break the third while loop
                        break  # We break the second while loop
                break  # We break from the first while loop since we are done

            line_index -= 1  # We didn't find the day string

    # If we arrive here, we check if we found a write position
    if write_position_normal == -1:
        # We did not find a day string.
        # So we add a new section at the bottom
        line_index = len(all_lines_host_normal) - 1

        while True:

            if line_index <= 0 or line_index >= len(all_lines_host_normal):
                break

            # Find end of blacklist, then create a new tag
            if "# END of Blacklist" in all_lines_host_normal[line_index]:
                line_index -= 1

                # Insert day string with some blank lines
                all_lines_host_normal.insert(line_index, f"# {day_string}\n")

                all_lines_host_normal.insert(line_index+1, f"\n")

                all_lines_host_normal.insert(line_index, f"\n")

                write_position_normal = line_index + 2
                break # We have our write position

            line_index -= 1

    # If we arrive here, we check if we found a write position for the txt version
    if write_position_txt == -1:
        # We did not find a day string.
        # So we add a new section at the bottom
        line_index = len(all_lines_host_txt) - 1

        while True:

            if line_index <= 0 or line_index >= len(all_lines_host_txt):
                break

            # Find end of blacklist, then create a new tag
            if "# END of Blacklist" in all_lines_host_txt[line_index]:
                line_index -= 1

                # Insert day string with some blank lines
                all_lines_host_txt.insert(line_index, f"# {day_string}\n")

                all_lines_host_txt.insert(line_index + 1, f"\n")

                all_lines_host_txt.insert(line_index, f"\n")

                write_position_txt = line_index + 2
                break  # We have our write position

            line_index -= 1

    # At this point we should have hopefully the writing position to append our url to.

    all_lines_host_normal.insert(write_position_normal, f"0.0.0.0 {url}\n")
    all_lines_host_txt.insert(write_position_txt, f"{url}\n")

    # Now, we can write it back to files
    with open(FILE_NAME, "w") as file:
        file.writelines(all_lines_host_normal)

    with open(FILE_NAME_TXT_VERSION, "w") as file:
        file.writelines(all_lines_host_txt)


    # Finished adding the string
    print(f"\nAdded URL: {url} to {FILE_NAME} and {FILE_NAME_TXT_VERSION} at section {day_string}.\n")

def remove_url(url: str) -> None:
    """
    Remove url to a host list
    """

    file_name = "hosts"
    file_name_txt_version = "hosts.txt"

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

    # Text Version
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
    Prints all available commands to console
    """

    print("\nAll available commands: ")
    print("\t\t'h' or 'help'         : Shows all commands")
    print("\t\t'q', 'quit' or 'exit' : Quit the program")
    print("\t\t'add %url%'           : Adds url to list (%url% should be a valid url without http or https.)")
    print("\t\t'find %url%'          : Checks if url in list (%url% should be a valid url without http or https.)")
    print("\t\t'remove %url%'        : Remove url from list (%url% should be a valid url without http or https.)")
    print("\t\t'push'                : Pushes changes made to github/repository.")
    print("\t\t'pull'                : Pulls changes made to github/repository.")

    print("\n")

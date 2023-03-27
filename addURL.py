from datetime import datetime
import fileinput


def main():
    print("Running console... (Use 'q' or 'quit' to exit) ('h' or 'help' for all commands)\n")

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
            case _:
                complex_command_handling(user_input)


def complex_command_handling(command):
    if command[:3] == "add":
        # Test URL: tracking.india.miui.com
        add_url(command[4:])
    elif command[:4] == "find":
        find_url(command[5:])
    else:
        print(f"Unknown command '{command}'. ('h' or 'help' for all commands)\n")


def contains_http(url):
    """Checks if string contains http returns true if true"""
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


def find_url(url):
    """Prints if url in list"""
    file_name = "hosts"
    found = False

    if contains_http(url):
        print("ERROR: url contains 'http/s' and is not valid.")
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
        print(f"\n{url_to_find} is not in {file_name}.\n")


def add_url(url):
    """Add url to hosts list"""
    file_name = "hosts"

    text = ""

    if contains_http(url):
        print("ERROR: url contains 'http/s' and is not valid.")
        return

    with open(file_name, "r") as f:
        text = f.read()

        # Checks if url already in file.
        if url in text:
            print(f"Error: URL '{url}' already in list. \n")
            return

    # If not, then we get our current day.
    day_string = datetime.today().strftime('%d.%m.%Y')  # %Y-%m-%d
    # day_string = "3" + day_string[1:] # Test if you want to see if the day gets added.

    found = False
    if day_string in text:
        found = True
    else:
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

    print(f"\nAdded URL: {url} to {file_name} at section {day_string}.\n")


def help_print():
    """Prints all commands to console"""
    print("\nAll commands: ")
    print("\t\t'h' or 'help' : Shows all commands (currently)")
    print("\t\t'q' or 'quit' : Quit the program")
    print("\t\t'add %url%'   : Adds url to list (%url% should be a valid url without http or https.)")
    print("\t\t'find %url%'  : Checks if url in list (%url% should be a valid url without http or https.)")

    print("\n")


if __name__ == "__main__":
    main()

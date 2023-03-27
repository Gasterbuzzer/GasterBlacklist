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
    else:
        print(f"Unknown command '{command}'. ('h' or 'help' for all commands)\n")


def add_url(url):
    """Add url to hosts list"""
    file_name = "hosts"

    text = ""

    with open(file_name, "r") as f:
        text = f.read()

        # Checks if url already in file.
        if url in text:
            print(f"Error: URL '{url}' already in list. \n")
            return

    # If not, then we get our current day.
    day_string = datetime.today().strftime('%d.%m.%Y')  # %Y-%m-%d
    found = False
    if day_string in text:
        print("Day String Found")
        found = True
    else:
        # Create day comment
        print(f"Day String not Found: {day_string}")

    for line in fileinput.input(files=file_name, inplace=True):
        print(f'{line}', end='')

        if f"# {day_string}" in line:
            # Adding URL
            print(f"0.0.0.0 {url}")




def help_print():
    """Prints all commands to console"""
    print("\nAll commands: ")
    print("\t\t'h' or 'help' : Shows all commands (currently)")
    print("\t\t'q' or 'quit' : Quit the program")
    print("\t\t'add'         : Adds url to list")  # (%url% should be a valid url without http or https.)

    print("\n")


if __name__ == "__main__":
    main()

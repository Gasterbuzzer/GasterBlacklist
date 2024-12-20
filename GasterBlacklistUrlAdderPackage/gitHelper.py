"""
Contains help for git commands such as pull and push.
"""

import subprocess
from datetime import datetime

class GitHelper:
    """
    Small Static helper class for git commands such as pull and push.
    """

    @staticmethod
    def check_git_install() -> bool:
        """
        Checks if git is installed.
        :return: True if git is installed, False otherwise.
        """

        # Running under try incase the command is not found.
        try:
            # Run "git --version"
            process = subprocess.Popen(["git", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            _, error = process.communicate()

            if process.returncode == 0:
                return True # Git is installed
            else: # Git command failed or did not finish, which could mean that git is not installed.
                print("WARNING: 'git' is not installed. This will cause git related commands to fail.\n"
                      "If this is intentional, you can ignore this warning safely.\n")
                return False

        except FileNotFoundError:
            # We assume git as not installed
            # So we print that it does not exist
            print("WARNING: 'git' is not installed. This will cause git related commands to fail.\n"
                  "If this is intentional, you can ignore this warning safely.\n")
            return False


    @staticmethod
    def pull_git() -> bool:
        """
        Pulls git to get the newest changes.
        :return: True if was able to run without errors and false if not. Is used for debugging.
        """

        # Check if git is installed and if not cancel the operation.
        if not GitHelper.check_git_install():
            return False

        # Run "git pull" at current location.
        process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
        output = process.communicate()[0].decode('utf-8').strip()

        print(f"\nDebug: Git Pull Status:\n '{output}'.\n")
        return True # Errorless execution

    @staticmethod
    def commit_changes_git() -> None:
        """
        Commits current changes host file to git.
        """

        # Check if git is installed and if not cancel the operation.
        if not GitHelper.check_git_install():
            return

        # Run "git add" at the current location for the host files.
        process = subprocess.Popen(["git", "add", ".\\hosts"], stdout=subprocess.PIPE)
        output_1 = process.communicate()[0].decode('utf-8').strip()
        process = subprocess.Popen(["git", "add", ".\\hosts.txt"], stdout=subprocess.PIPE)
        output_2 = process.communicate()[0].decode('utf-8').strip()

        print(f"\nDebug: Added elements hosts and hosts.txt to git: '{output_1}' and '{output_2}'.\n")

        # Run "git commit -m 'current date'" at the current location.
        # Get the current date as a commit message
        day_string = datetime.today().strftime('%d.%m.%Y')  # %Y-%m-%d

        process = subprocess.Popen(["git", "commit", "-m", day_string], stdout=subprocess.PIPE)
        output = process.communicate()[0].decode('utf-8').strip()

        print(f"\nDebug: Commited changes to git: '{output}'.\n")

    @staticmethod

    def push_changes_git() -> None:
        """
        Pushes current changes to git.
        """

        # Check if git is installed and if not cancel the operation.
        if not GitHelper.check_git_install():
            return

        # Run "git push" at the current location.
        process = subprocess.Popen(["git", "push"], stdout=subprocess.PIPE)
        output = process.communicate()[0].decode('utf-8').strip()

        print(f"\nDebug: Pushed changes with git: '{output}'.\n")

    @staticmethod
    def upload_changes() -> None:
        """
        Commits and Pushes current changes.
        Gets cancelled if no git installation was found.
        """

        # Check if git is installed and if not cancel the operation.
        if not GitHelper.check_git_install():
            return

        # (First pull) And then Commit and push changes
        GitHelper.pull_git() # Ensures we have the newest changes before commiting
        GitHelper.commit_changes_git()
        GitHelper.push_changes_git()
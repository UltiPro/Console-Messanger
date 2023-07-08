import os
from colorama import init, Fore, Style


class ConsoleMessanger():
    def __init__(self):
        init(convert=True)

    def _print_system_information(self, message):
        print(Fore.GREEN + "{}".format(message) + Style.RESET_ALL)

    def _print_system_command(self, message):
        print(Fore.YELLOW + "{}".format(message) + Style.RESET_ALL)

    def _print_system_error(self, message):
        print(Fore.RED + "{}".format(message) + Style.RESET_ALL)

    def _console_clear(self):
        os.system('cls' if os.name == "nt" else "clear")

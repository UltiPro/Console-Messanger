import os
from colorama import init, Fore, Style


class ConsoleMessanger():
    def __init__(self):
        init(convert=True)

    def _clear_console(self):
        os.system('cls' if os.name == "nt" else "clear")

    def _print_system_information(self, message):
        print(Fore.GREEN + "{}".format(message) + Style.RESET_ALL)

    def _print_system_information_light(self, message):
        print(Fore.LIGHTGREEN_EX + "{}".format(message) + Style.RESET_ALL)

    def _print_system_command(self, message):
        print(Fore.YELLOW + "{}".format(message) + Style.RESET_ALL)

    def _print_system_command_light(self, message):
        print(Fore.LIGHTYELLOW_EX + "{}".format(message) + Style.RESET_ALL)

    def _print_system_error(self, message):
        print(Fore.RED + "{}".format(message) + Style.RESET_ALL)

    def _print_system_error_light(self, message):
        print(Fore.LIGHTRED_EX + "{}".format(message) + Style.RESET_ALL)

    def _print_system_server_message(self, message):
        print(Fore.BLUE + "{}".format(message) + Style.RESET_ALL)

    def _print_system_private_message(self, message):
        print(Fore.MAGENTA + "{}".format(message) + Style.RESET_ALL)

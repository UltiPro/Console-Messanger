import os
from colorama import init, Fore, Style


class ConsoleMessanger():
    def __init__(self):
        init(convert=True)

    def _clear_console(self):
        os.system('cls' if os.name == "nt" else "clear")

    def _print_system_information(self, message):
        print(Fore.LIGHTGREEN_EX + "{}".format(message) + Style.RESET_ALL)

    def _print_system_command(self, message):
        print(Fore.LIGHTYELLOW_EX + "{}".format(message) + Style.RESET_ALL)

    def _print_system_command2(self, message):
        print(Fore.YELLOW + "{}".format(message) + Style.RESET_ALL)

    def _print_system_error(self, message):
        print(Fore.LIGHTRED_EX + "{}".format(message) + Style.RESET_ALL)

    def _print_system_ban(self, message):
        print(Fore.RED + "{}".format(message) + Style.RESET_ALL)

    def _print_system_unban(self, message):
        print(Fore.GREEN + "{}".format(message) + Style.RESET_ALL)

    def _print_system_server_message(self, message):
        print(Fore.LIGHTBLUE_EX + "{}".format(message) + Style.RESET_ALL)

    def _print_system_private_message(self, message):
        print(Fore.LIGHTMAGENTA_EX + "{}".format(message) + Style.RESET_ALL)

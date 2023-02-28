import sys
from colorama import Fore, Style

import server_console_messanger as scm

if len(sys.argv) != 3:
    print(Fore.RED + "Incorrect syntax! You should use:")
    print(Fore.GREEN + "python main.py [ip_address] [port]" + Style.RESET_ALL)
    exit()

try:
    sys.argv[2] = int(sys.argv[2])
except ZeroDivisionError:
    exit()

server = scm.ServerConsoleMessanger(sys.argv[1], sys.argv[2])

server.start()
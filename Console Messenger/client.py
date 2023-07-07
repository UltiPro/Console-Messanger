import sys

from main.clientApp import ClientConsoleMessanger

client = None

if len(sys.argv) == 1:
    client = ClientConsoleMessanger()
elif len(sys.argv) == 2:
    client = ClientConsoleMessanger(sys.argv[1])
elif len(sys.argv) == 3:
    client = ClientConsoleMessanger(sys.argv[1], sys.argv[2])
elif len(sys.argv) == 4:
    client = ClientConsoleMessanger(sys.argv[1], sys.argv[2], int(sys.argv[3]))

client.start()

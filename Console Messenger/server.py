import sys

from main.serverApp import ServerConsoleMessanger

server = None

if len(sys.argv) == 1:
    server = ServerConsoleMessanger()
elif len(sys.argv) == 2:
    server = ServerConsoleMessanger(sys.argv[1])
elif len(sys.argv) == 3:
    server = ServerConsoleMessanger(sys.argv[1], sys.argv[2])

server.start()

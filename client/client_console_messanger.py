import socket, select, sys

class Client():
    def __init__(self, ip_address = "127.0.0.1", port = 25565):
        self.__ip_address = ip_address
        self.__port = port
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.__server.connect((self.__ip_address, self.__port))
        while True:

            sockets_list = [sys.stdin, self.__server]
        
            read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
        
            for socks in read_sockets:
                if socks == self.__server:
                    message = socks.recv(2048)
                    print (message)
                else:
                    message = sys.stdin.readline()
                    self.__server.send(message)
                    sys.stdout.write("<You>")
                    sys.stdout.write(message)
                    sys.stdout.flush()
        else:
            self.server.close()

    def stop(self):
        pass
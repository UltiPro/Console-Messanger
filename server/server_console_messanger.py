import socket
from _thread import *


class ServerConsoleMessanger():
    def __init__(self, ip_address, port):
        self.__list_of_clients = []
        self.__ip_address = ip_address
        self.__port = port
        self.__running = True
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self, number_of_clients=100):
        print("start - start")

        # number_of_clients = int(number_of_clients) if number_of_clients.isnumeric() else 5 # dokończ

        self.__server.bind((self.__ip_address, int(self.__port)))
        self.__server.listen(number_of_clients)

        while True:
            connection, address = self.__server.accept()
            self.__list_of_clients.append(connection)
            print("{} connected".format(address[0]))
        else:
            connection.close()
            self.__server.close()

    def _new_client_thread(self, connection, address):
        connection.send("Welcome to chatroom at {}", self.__ip_address)
        while self.__running:
            try:
                message = connection.recv(2048)
                if message:
                    message_to_send = "<{}> {}".format(address[0], message)
                    print(message_to_send)
                    self._broadcast(message_to_send, connection)
                else:
                    self._remove_connection(connection)
            except:
                continue

    def _broadcast(self, message, connection):
        for client in self.__list_of_clients:
            if client != connection:
                try:
                    client.send(message)
                except:
                    client.close()
                    self._remove_connection(client)

    def _remove_connection(self, connection):
        if connection in self.__list_of_clients:
            self.__list_of_clients.remove(connection)

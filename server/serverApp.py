import socket
import threading


class ServerConsoleMessanger():
    def __init__(self, ip_address="127.0.0.1", port=50500):
        self.__ip_address = ip_address
        self.__port = port
        self.__clients_list = []
        self.__usernames_list = []
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__runningServer = True

    def start(self):
        self.__server.bind((self.__ip_address, self.__port))
        self.__server.listen()
        self._recive()

    def _broadcast(self, message):
        for client in self.__clients_list:
            client.send(message)

    def _handleUser(self, client):
        while self.__runningServer:
            try:
                message = client.recv(1024)
                self._broadcast(message)
            except:
                index_of_client = self.__clients_list.index(client)
                self.__clients_list.remove(client)
                client.close()
                nickname = self.__usernames_list[index_of_client]
                self._broadcast("User {} left the chat!".format(
                    nickname).encode("utf-8"))
                self.__usernames_list.remove(nickname)
                break

    def _recive(self):
        while self.__runningServer:
            client, address = self.__server.accept()
            print("Connected from {}".format(address))
            nickname = client.recv(1024).decode("utf-8")
            self.__usernames_list.append(nickname)
            self.__clients_list.append(client)
            self._broadcast("User {} has join the chat!".format(
                nickname).encode("utf-8"))
            handle_user_theard = threading.Thread(
                target=self._handleUser, args=(client, ))
            handle_user_theard.start()

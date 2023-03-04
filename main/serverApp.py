import socket
import threading

from rsa.rsaImplementation import RSAImplementation


class ServerConsoleMessanger():
    def __init__(self, ip_address="127.0.0.1", port=50500):  # dokończ
        self.__ip_address = ip_address
        self.__port = port
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__clients_list = []
        self.__usernames_list = []
        self.__rsa_client = RSAImplementation()  # dokończ
        self.__users_codes_list = []  # dokończ

    def start(self):
        self.__server.bind((self.__ip_address, self.__port))
        self.__server.listen()
        self._recive()

    def _broadcast(self, message):
        if message == "" or message == None:
            return
        idx = 0
        for client in self.__clients_list:
            e, n = self.__users_codes_list[idx]
            client.send(RSAImplementation.encrypt_msg_default(
                message, e, n).encode("utf-8"))
            idx += 1

    def _handleUser(self, client):
        while True:
            try:
                message = self.__rsa_client.decrypt_msg(
                    client.recv(1024).decode("utf-8"))
                self._broadcast(message)
            except:
                index_of_client = self.__clients_list.index(client)
                self.__clients_list.remove(client)
                self.__users_codes_list.remove(
                    self.__users_codes_list[index_of_client])
                client.close()
                nickname = self.__usernames_list[index_of_client]
                self._broadcast("User {} left the chat!".format(
                    nickname).encode("utf-8"))
                self.__usernames_list.remove(nickname)
                break

    def _recive(self):  # dokończ
        e, n = self.__rsa_client.public_key()
        while True:
            # try:
            client, address = self.__server.accept()
            print("Connected from {}".format(address))
            init_data = client.recv(1024).decode("utf-8").split("$$$$")
            self.__clients_list.append(client)
            self.__usernames_list.append(init_data[0])
            self.__users_codes_list.append(
                (int(init_data[1]), int(init_data[2])))
            client.send("{}$$$${}".format(
                e, n).encode("utf-8"))
            self._broadcast("User {} has join the chat!".format(
                init_data[0]))
            handle_user_theard = threading.Thread(
                target=self._handleUser, args=(client, ))
            handle_user_theard.start()
            # except:
            #    print("Incorrect data from {}, client data {}".format(
            #        address, client))

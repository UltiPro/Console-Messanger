import socket
import threading

from rsa.rsaImplementation import RSAImplementation


class ClientConsoleMessanger():
    def __init__(self, server_address="127.0.0.1", server_port=50500, nickname="Undefined"):  # dokończ
        self.__server_address = server_address
        self.__server_port = server_port
        self.__nickname = nickname
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__rsa_client = RSAImplementation()
        self.__server_public_key_e = None
        self.__server_public_key_n = None

    def start(self):
        print("Connecting to server...")
        self.__client.connect((self.__server_address, self.__server_port))
        e, n = self.__rsa_client.public_key()
        self.__client.send("{}$$$${}$$$${}".format(
            self.__nickname, e, n).encode("utf-8"))
        self.__server_public_key_e, self.__server_public_key_n = self.__client.recv(
            1024).decode("utf-8").split("$$$$")
        self.__server_public_key_e = int(self.__server_public_key_e)
        self.__server_public_key_n = int(self.__server_public_key_n)

        recive_Theard = threading.Thread(target=self._recive)
        recive_Theard.start()

        write_Theard = threading.Thread(target=self._write)
        write_Theard.start()

    def _recive(self):
        while True:
            try:
                message = self.__rsa_client.decrypt_msg(
                    self.__client.recv(1024).decode("utf-8"))
                print(message)
            except ConnectionError:
                print("Connection error. Stopping client...")
                self.__client.close()
                break

    def _write(self):
        while True:
            try:
                message = "<{}>: {}".format(self.__nickname, input())
                self.__client.send(RSAImplementation.encrypt_msg_default(
                    message, self.__server_public_key_e, self.__server_public_key_n).encode("utf-8"))
            except ConnectionError:
                print("Connection error. Stopping client...")
                self.__client.close()
                break
            except EOFError:
                print("Ctrl + C -> Stopping client...")
                self.__client.close()
                break

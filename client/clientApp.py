import socket
import threading


class ClientConsoleMessanger():
    def __init__(self, server_address="127.0.0.1", server_port=50500, nickname="Undefined"):
        self.__server_address = server_address
        self.__server_port = server_port
        self.__nickname = nickname
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        print("Connecting to server...")
        self.__client.connect((self.__server_address, self.__server_port))
        self.__client.send(self.__nickname.encode("utf-8"))

        recive_Theard = threading.Thread(target=self._recive)
        recive_Theard.start()

        write_Theard = threading.Thread(target=self._write)
        write_Theard.start()

    def _recive(self):
        while True:
            try:
                message = self.__client.recv(1024).decode("utf-8")
                print(message)
            except ConnectionError:
                print("Connection error. Stopping client...")
                self.__client.close()
                break

    def _write(self):
        while True:
            try:
                message = "<{}>: {}".format(self.__nickname, input())
                self.__client.send(message.encode("utf-8"))
            except ConnectionError:
                print("Connection error. Stopping client...")
                self.__client.close()
                break
            except EOFError:
                print("Ctrl + C -> Stopping client...")
                self.__client.close()
                break

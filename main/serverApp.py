import socket
from colorama import init, Fore, Style

from thread.stoppableThread import StoppableThread
from rsa.rsaImplementation import RSAImplementation


class ServerConsoleMessanger():
    def __init__(self, ip_address="127.0.0.1", port=50500):
        self.__ip_address = ip_address
        self.__port = port
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__rsa_client = RSAImplementation()
        self.__clients_list = []
        self.__usernames_list = []
        self.__users_codes_list = []
        self.__user_theards_list = []
        self.__recive_Theard = None
        self.__running = True
        init(convert=True)

    def start(self):
        try:
            self.__server.bind((self.__ip_address, self.__port))
            self.__server.listen()
        except OSError:
            self._print_system_error(
                "Port {} is occupied. Server stopped...".format(self.__port))
            return
        self.__recive_Theard = StoppableThread(target=self._recive)
        while True:
            cmd = input("Stop server? Type: /stop\n")
            if cmd == "/stop":
                for theard in self.__user_theards_list:
                    theard.stop()
                self.__recive_Theard.stop()
                self._print_system_info("Stopping server...")
                exit(0)
            else:
                self._print_system_error("Unknown command. Try again.")

    def _broadcast(self, message, skip_client):
        if message == "":
            return
        idx = 0
        for client in self.__clients_list:
            if client is skip_client:
                continue
            e, n = self.__users_codes_list[idx]
            client.send(RSAImplementation.encrypt_msg_default(
                message, e, n).encode("utf-8"))
            idx += 1

    def _handleUser(self, client):
        while self.__running:
            try:
                message = self.__rsa_client.decrypt_msg(
                    client.recv(1024).decode("utf-8"))
                self._broadcast(message, None)
            except:
                index_of_client = self.__clients_list.index(client)
                self.__clients_list.remove(client)
                self.__users_codes_list.remove(
                    self.__users_codes_list[index_of_client])
                self.__user_theards_list.remove(
                    self.__user_theards_list[index_of_client])
                client.close()
                nickname = self.__usernames_list[index_of_client]
                self._broadcast("Info: User {} left the chat!".format(
                    nickname).encode("utf-8"), None)
                self._print_system_info(
                    "User {} disconnected".format(nickname))
                self.__usernames_list.remove(nickname)
                break

    def _recive(self):
        e, n = self.__rsa_client.public_key()
        while self.__running:
            client, address = self.__server.accept()
            init_data = client.recv(1024).decode("utf-8").split("$$$$")
            self.__clients_list.append(client)
            self.__usernames_list.append(init_data[0])
            self.__users_codes_list.append(
                (int(init_data[1]), int(init_data[2])))
            self._print_system_info(
                "User {}, connected from {}".format(init_data[0], address))
            client.send("{}$$$${}".format(
                e, n).encode("utf-8"))
            self._broadcast("Info: User {} has join the chat!".format(
                init_data[0]), client)
            handle_user_theard = StoppableThread(
                target=self._handleUser, args=(client, ))
            handle_user_theard.start()
            self.__user_theards_list.append(handle_user_theard)

            # try:
            # except:
            #   print("Incorrect data from {}, client data {}".format(address, client))

    def _print_system_info(self, message):
        print(Fore.GREEN + "{}".format(message) + Style.RESET_ALL)

    def _print_system_error(self, message):
        print(Fore.RED + "{}".format(message) + Style.RESET_ALL)

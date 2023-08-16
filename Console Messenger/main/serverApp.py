import socket

from main.app import ConsoleMessanger
from thread.stoppableThread import StoppableThread
from rsa.rsaImplementation import RSAImplementation


class ServerConsoleMessanger(ConsoleMessanger):
    def __init__(self, ip_address="127.0.0.1", port=50500):
        self.__ip_address = ip_address
        self.__port = int(port)
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__rsa_client = RSAImplementation()
        self.__clients_list = []
        self.__usernames_list = []
        self.__users_codes_list = []
        self.__user_theards_list = []
        self.__admins_list = []
        self.__recive_theard = None
        self.__running = True

    def start(self):
        self._console_clear()
        try:
            self.__server.bind((self.__ip_address, self.__port))
            self.__server.listen()
        except OSError:
            self._print_system_error(
                "Port {} is occupied. Server stopped...".format(self.__port))
            return
        self.__recive_theard = StoppableThread(target=self._recive)
        self.__recive_theard.start()
        while self.__running:
            try:
                cmd = input(
                    "Type command: (/help for more information)\n").split(" ")
                match cmd[0]:
                    case "/server":
                        try:
                            match cmd[1]:
                                case "stop":
                                    self._stop()
                                    break
                                case "clear":
                                    self._console_clear()
                                    self._print_system_information(
                                        "Console cleared... ")
                                case _:
                                    raise IndexError
                        except IndexError:
                            self._print_system_error(
                                "This command requires parameter. Try again.")
                    case "/kick":
                        try:
                            self._close_connection(
                                self.__clients_list[self.__usernames_list.index(cmd[1])])
                            self._broadcast(
                                "Info: User {} has been kicked from the chat!".format(cmd[1]), None)
                        except ValueError:
                            self._print_system_command(
                                "The given nickname does not match any user. Try again.")
                        except IndexError:
                            self._print_system_error(
                                "This command requires parameter. Try again.")
                    case "/admin":
                        try:
                            self.__admins_list.append(
                                self.__clients_list[self.__usernames_list.index(cmd[1])])
                            self._broadcast(
                                "Info: User {} has been given admin permissions!".format(cmd[1]), None)
                            self._print_system_information(
                                "Info: User {} has been given admin permissions!".format(cmd[1]))
                        except ValueError:
                            self._print_system_command(
                                "The given nickname does not match any user. Try again.")
                        except IndexError:
                            self._print_system_error(
                                "This command requires parameter. Try again.")
                    case "/help":
                        self._print_help_info()
                    case _:
                        self._print_system_error("Unknown command. Try again.")
            except KeyboardInterrupt:
                self._stop()
                break
        exit(0)

    def _recive(self):
        e, n = self.__rsa_client.public_key()
        client = None
        while self.__running:
            try:
                client, address = self.__server.accept()
                init_data = client.recv(1024).decode("utf-8").split("$$$$")
                if init_data[0] in self.__usernames_list:
                    client.close()
                client.send("{}$$$${}".format(
                    e, n).encode("utf-8"))
                self.__clients_list.append(client)
                self.__usernames_list.append(init_data[0])
                self.__users_codes_list.append(
                    (int(init_data[1]), int(init_data[2])))
                self._print_system_information(
                    "User {}, connected from {}".format(init_data[0], address))
                self._broadcast("Info: User {} has join the chat!".format(
                    init_data[0]), client)
                handle_user_theard = StoppableThread(
                    target=self._handleUser, args=(client, ))
                self.__user_theards_list.append(handle_user_theard)
                handle_user_theard.start()
            except ValueError:
                if client and address:
                    self._print_system_command("Incorrect data from client {} {}".format(
                        address, client))
                else:
                    break
            except (OSError, UnboundLocalError):
                if client:
                    self._close_connection(client)
                else:
                    break

    def _handleUser(self, client):
        while self.__running:
            try:
                message = self.__rsa_client.decrypt_msg(
                    client.recv(1024).decode("utf-8"))
                message_command = message.split(" ")
                if (message_command[1].startswith("/")):
                    client = self.__clients_list[self.__usernames_list.index(
                        message_command[0][1:-2])]
                    match message_command[1]:
                        case "/kick":
                            if (client in self.__admins_list):
                                try:
                                    self._close_connection(
                                        self.__clients_list[self.__usernames_list.index(message_command[2])])
                                    self._broadcast("Info: User {} has been kicked from the chat by admin {}!".format(
                                        message_command[2], message_command[0][1:-2]), None)
                                except ValueError:
                                    client.send(
                                        "Info: The given nickname does not match any user. Try again.".encode("utf-8"))
                                except IndexError:
                                    client.send(
                                        "Info: This command requires parameter. Try again.".encode("utf-8"))
                            else:
                                client.send(
                                    "Info: This command requires admin permissions.".encode("utf-8"))
                else:
                    self._broadcast(message, None)
            except (ConnectionAbortedError, ConnectionResetError, ConnectionError):
                if client in self.__clients_list:
                    self._close_connection(client)
                break

    def _broadcast(self, message, skip_client):
        if message == "":
            return
        idx = 0
        for client in self.__clients_list:
            if client is skip_client:
                continue
            e, n = self.__users_codes_list[idx]
            try:
                client.send(RSAImplementation.encrypt_msg_default(
                    message, e, n).encode("utf-8"))
                idx += 1
            except (ConnectionAbortedError, ConnectionResetError, ConnectionError):
                continue

    def _close_connection(self, client):
        if client not in self.__clients_list:
            return
        index_of_client = self.__clients_list.index(client)
        nickname = self.__usernames_list[index_of_client]
        theard = self.__user_theards_list[index_of_client]
        self.__usernames_list.remove(nickname)
        self.__users_codes_list.remove(
            self.__users_codes_list[index_of_client])
        self.__user_theards_list.remove(theard)
        self.__clients_list.remove(client)
        if client in self.__admins_list:
            self.__admins_list.remove(client)
            self._print_system_information(
                "Admin {} disconnected.".format(nickname))
            self._broadcast(
                "Info: Admin {} left the chat!".format(nickname), None)
        else:
            self._print_system_information(
                "User {} disconnected.".format(nickname))
            self._broadcast(
                "Info: User {} left the chat!".format(nickname), None)
        client.close()
        theard.stop()

    def _stop(self):
        self.__running = False
        self.__recive_theard.stop()
        for client in self.__clients_list:
            self._close_connection(client)
        self._print_system_information("Stopping server...")
        self.__server.close()

    def _print_help_info(self):
        self._print_system_command("/server stop -> closes server")
        self._print_system_command("/server clear -> clears console")
        self._print_system_command(
            "/kick [nickname] -> kicks user from server")
        self._print_system_command(
            "/admin [nickname] -> gives user admin permissions")
        self._print_system_command("/help -> prints commands informations")

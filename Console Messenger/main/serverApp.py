import socket

from main.app import ConsoleMessanger
from main.exceptions import *
from thread.stoppableThread import StoppableThread
from rsa.rsaImplementation import RSAImplementation


class ServerConsoleMessanger(ConsoleMessanger):
    def __init__(self, ip_address="127.0.0.1", port=50500):
        self.__ip_address = ip_address
        self.__port = int(port)
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__rsa_client = RSAImplementation()
        self.__receive_connection_thread = None
        self.__running = True
        self.__clients_list = []
        self.__clients_nicknames_list = []
        self.__clients_codes_list = []
        self.__clients_threads_list = []
        self.__clients_admins_list = []
        self.__banned_nicknames_list = []
        self.__banned_ips_list = []

    def start(self):
        self._clear_console()
        try:
            self.__server.bind((self.__ip_address, self.__port))
            self.__server.listen()
        except OSError:
            self._print_system_error(
                "Port '{}' is occupied. Server stopped...".format(self.__port))
            return
        self.__receive_connection_thread = StoppableThread(
            target=self._receive_connection)
        self.__receive_connection_thread.start()
        while self.__running:
            try:
                cmd = input(
                    "(Type /help for more informations)\nType command: ").split(" ")
                match cmd[0]:
                    case "/stop":
                        self._stop()
                    case "/clear":
                        self._clear_console()
                        self._print_system_information("Console cleared... ")
                    case "/msg":
                        message = " ".join(cmd[1:]).strip()
                        if (message == ""):
                            raise IndexError
                        self._command_msg(message)
                    case "/kick":
                        if (cmd[1].replace(" ", "") == ""):
                            raise IndexError
                        self._command_kick(cmd[1])
                    # tutaj
                    case "/admin":
                        if (cmd[1].replace(" ", "") == ""):
                            raise IndexError
                        self._command_admin(cmd[1])
                        print(self.__clients_admins_list) # test only
                    case "/unadmin":
                        if (cmd[1].replace(" ", "") == ""):
                            raise IndexError
                        self._command_unadmin(cmd[1])
                    case "/ban":
                        if (cmd[1].replace(" ", "") == ""):
                            raise IndexError
                        self._command_ban(cmd[1])
                    case "/unban":
                        if (cmd[1].replace(" ", "") == ""):
                            raise IndexError
                        self._command_unban(cmd[1])
                    case "/list":
                        if (cmd[1].replace(" ", "") == ""):
                            raise IndexError
                        self._command_list(cmd[1])
                    case "/help":
                        self._command_help()
                    case _:
                        self._print_system_error("Unknown command. Try again.")
            except IndexError:
                self._print_system_error(
                    "This command requires parameter. Try again.")
            except KeyboardInterrupt:
                self._stop()
                break
            # tutaj
        exit(0)

    def _receive_connection(self):
        e, n = self.__rsa_client.public_key()
        while self.__running:
            try:
                client, address = self.__server.accept()
                init_data = client.recv(1024).decode("utf-8").split("$$$$")
                client.send("{}$$$${}".format(e, n).encode("utf-8"))
                if (init_data[0] in self.__banned_nicknames_list):
                    raise BannedUserNickname
                if (address[0] in self.__banned_ips_list):
                    raise BannedUserIp
                if (init_data[0] in self.__clients_nicknames_list):
                    raise NicknameAlreadyTaken
                self.__clients_list.append(client)
                self.__clients_nicknames_list.append(init_data[0])
                self.__clients_codes_list.append(
                    (int(init_data[1]), int(init_data[2])))
                self.__clients_threads_list.append(StoppableThread(
                    target=self._handle_client, args=(client, )))
                self.__clients_threads_list[-1].start()
                self._print_system_information(
                    "User '{}' connected from '{}'.".format(init_data[0], address))
                self._broadcast(
                    "Info: {} has join the chat.".format(init_data[0]), client)
                # tutaj
            except BannedUserNickname:
                self._print_system_error(
                    "Connection from '{}' rejected. Nickname '{}' is banned.".format(address[0], init_data[0]))
                client.send("Error: Your nickname is banned at this server.")
                client.close()
            except BannedUserIp:
                self._print_system_error(
                    "Connection from '{}' rejected. Address IP banned.".format(address[0]))
                client.send("Error: You are banned at this server.")
                client.close()
            except NicknameAlreadyTaken:
                client.send(
                    "Info: This nickname is already taken. Choose another one.")
                client.close()
                # tutaj
            except OSError:
                break
            '''except (ConnectionError, ConnectionResetError, ConnectionAbortedError):
                if client in self.__clients_list:
                    self._close_connection(client)
                else:
                    client.close()
            except (OSError, UnboundLocalError, ValueError):
                if client and address:
                    self._print_system_error(
                        "Incorrect data from '{}', connection denied. More client info: {}.".format(address, client))
                    client.send(
                        "Error: Server connection error. Connection denied.")
                    if client in self.__clients_list:
                        self._close_connection(client)
                    else:
                        client.close()
                else:
                    break'''

    def _handle_client(self, client):
        nickname = self.__clients_nicknames_list[self.__clients_list.index(
            client)]
        while self.__running:
            try:
                message = self.__rsa_client.decrypt_msg(
                    client.recv(1024).decode("utf-8"))
                if (message.startswith("/")):
                    message_command = message.split(" ")
                    match message_command[0]:
                        # tutaj
                        case "/kick":
                            if (client not in self.__clients_admins_list):
                                raise UnauthorizedError
                            if (message_command[1].replace(" ", "") == ""):
                                raise IndexError
                            self._command_kick(message_command[1], client)
                        case "/ban":
                            if (client not in self.__clients_admins_list):
                                raise UnauthorizedError
                            if (message_command[1].replace(" ", "") == ""):
                                raise IndexError
                            # self._command_ban(cmd[1])
                        case "/unban":
                            if (client not in self.__clients_admins_list):
                                raise UnauthorizedError
                            if (message_command[1].replace(" ", "") == ""):
                                raise IndexError
                            # self._command_unban(cmd[1])
                        case "/list":
                            if (message_command[1].replace(" ", "") == ""):
                                raise IndexError
                            # self._command_list(cmd[1])
                        case "/pv":
                            if (message_command[1].replace(" ", "") == "" or message_command[2].replace(" ", "") == ""):
                                self._send_to(
                                    client, "Error: This command requires two parameters (/pv [nickname] [message]). Try again.")
                            else:
                                pass  # to
                        case _:
                            self._send_to(
                                client, "Error: Unknown command. Try again.")
                else:
                    self._broadcast("<{}>: {}".format(nickname, message), None)
            except UnauthorizedError:
                self._send_to(
                    client, "Info: This command requires admin permissions.")
            except IndexError:
                self._send_to(
                    client, "Error: This command requires parameter. Try again.")
            except (ConnectionError, ConnectionResetError, ConnectionAbortedError, OSError):
                self._close_connection(client)
                break
            # tutaj

    def _broadcast(self, message, skip_client):
        if message == "":
            return
        for idx, client in enumerate(self.__clients_list):
            if client is skip_client:
                continue
            try:
                e, n = self.__clients_codes_list[idx]
                client.send(RSAImplementation.encrypt_msg_default(
                    message, e, n).encode("utf-8"))
            except (ConnectionError, ConnectionResetError, ConnectionAbortedError):
                self._close_connection(client)  # to
            '''except ValueError:
                continue
            '''

    def _send_to(self, to_client, message):
        if message == "":
            return
        try:
            e, n = self.__clients_codes_list[self.__clients_list.index(
                to_client)]
            to_client.send(RSAImplementation.encrypt_msg_default(
                message, e, n).encode("utf-8"))
        except (ConnectionAbortedError, ConnectionResetError, ConnectionError):
            pass  # to
        '''except ValueError:
                continue
            '''

    def _stop(self):
        self._print_system_information("Stopping the server...")
        self.__running = False
        self.__receive_connection_thread.stop()
        while (self.__clients_list.__len__() > 0):
            for client in self.__clients_list:
                self._close_connection(client)
        self.__server.close()
        self._print_system_information("Server stopped.")

    def _close_connection(self, client):
        if client not in self.__clients_list:
            return
        index = self.__clients_list.index(client)
        nickname = self.__clients_nicknames_list[index]
        thread = self.__clients_threads_list[index]
        self.__clients_list.remove(client)
        self.__clients_nicknames_list.remove(nickname)
        self.__clients_codes_list.remove(self.__clients_codes_list[index])
        self.__clients_threads_list.remove(thread)
        # to
        if client in self.__clients_admins_list:
            self.__clients_admins_list.remove(client)
            self._print_system_information(
                "Admin '{}' disconnected.".format(nickname))
            self._broadcast(
                "Info: Admin {} left the chat!".format(nickname), None)
        else:
            self._print_system_information(
                "User '{}' disconnected.".format(nickname))
            self._broadcast(
                "Info: User {} left the chat!".format(nickname), None)
        # to
        client.close()
        thread.stop()

    def _command_msg(self, msg):
        msg = ">Server<: {}".format(msg)
        self._broadcast(msg, None)
        self._print_server_message(msg)

    def _command_kick(self, nickname, client=None):
        try:
            self._close_connection(
                self.__clients_list[self.__clients_nicknames_list.index(nickname)])
            self._broadcast(
                "Info: {} has been kicked from the chat!".format(nickname), None)
        except ValueError:
            if client:
                self._send_to(
                    client, "Info: The given nickname does not match any user. Try again.")
            else:
                self._print_system_command(
                    "The given nickname does not match any user. Try again.")

    def _command_admin(self, nickname):
        try:
            self.__clients_admins_list.append(
                self.__clients_list[self.__clients_nicknames_list.index(nickname)])
            self._broadcast(
                "Info: {} has been given admin permissions!".format(nickname), None)
            self._print_system_information(
                "Info: '{}' has been given admin permissions!".format(nickname))
        except ValueError:
            self._print_system_command(
                "The given nickname does not match any user. Try again.")

    def _command_unadmin(self, nickname):
        try:
            self.__clients_admins_list.remove(
                self.__clients_list[self.__clients_nicknames_list.index(nickname)])
            self._broadcast(
                "Info: {} has lost admin permissions!".format(nickname), None)
            self._print_system_information(
                "Info: '{}' has lost admin permissions!".format(nickname))
        except ValueError:
            self._print_system_command(
                "The given nickname does not match any admin. Try again.")

    # tutaj
    def _command_ban(self, nickname):
        try:
            client = self.__clients_list[self.__clients_nicknames_list.index(
                nickname)]
            self.__banned_ips_list.append(client.getpeername()[0])
            self._close_connection(client)
            self._broadcast(
                "Info: User {} has been banned from the chat!".format(user_nickname), None)
            self._print_system_information(
                "Info: User {} has been banned from the chat!".format(user_nickname))
        except ValueError:
            self._print_system_command(
                "The given nickname does not match any user. Try again.")
        except IndexError:
            self._print_system_error(
                "This command requires parameter. Try again.")

    def _command_unban(self, user_nickname):
        pass

    def _command_list(self, command, client):
        message_title = ""
        message = ""
        match command:
            case "users":
                message_title = "Connected users list:"
                for nickname in self.__clients_nicknames_list:
                    message = "{} ".format(nickname)
            case "admins":
                message_title = "Connected admins list:"
                for admin in self.__clients_admins_list:
                    nickname = self.__clients_nicknames_list(
                        self.__clients_list.index(admin))
                    message = "{} ".format(nickname)
            case "banned":
                self._print_system_information("\nBanned users list:\n")
                for banned in self.__banned_nicknames_list:
                    self._print_system_error(banned+" ")
            case "banned_ip":
                self._print_system_information("\nBanned ip list:\n")
                for banned_ip in self.__banned_ips_list:
                    self._print_system_error(banned_ip+" ")
            case _:
                self._print_system_command(
                    "The given parameter does not match any type. Try again.")

    def _command_help(self):
        self._print_system_command("/stop -> closes server")
        self._print_system_command("/clear -> clears console")
        self._print_system_command(
            "/msg [message] -> sends server message to all")
        self._print_system_command(
            "/kick [nickname] -> kicks user from server")
        self._print_system_command(
            "/admin [nickname] -> gives user admin permissions")
        self._print_system_command("/help -> prints commands informations")
    # tutaj

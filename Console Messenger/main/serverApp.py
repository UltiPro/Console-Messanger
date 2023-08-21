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
                "Could not use given IP address or port '{}' is occupied. Server stopped...".format(self.__port))
            return
        except OverflowError:
            self._print_system_error("Port needs to be between 0-65535.")
            return
        self.__receive_connection_thread = StoppableThread(
            target=self._receive_connection)
        self.__receive_connection_thread.start()
        while self.__running:
            try:
                cmd = input(
                    "Type command: (Type /help for more informations)\n").split(" ")
                match cmd[0]:
                    case "/stop":
                        self._stop()
                    case "/clear":
                        self._clear_console()
                        self._print_system_command("Console cleared... ")
                    case "/msg":
                        message = " ".join(cmd[1:]).strip()
                        if message == "":
                            raise IndexError
                        self._command_msg(message)
                    case "/kick":
                        if cmd[1].replace(" ", "") == "":
                            raise IndexError
                        self._command_kick(cmd[1], None)
                    case "/admin":
                        if cmd[1].replace(" ", "") == "":
                            raise IndexError
                        self._command_admin(cmd[1])
                    case "/unadmin":
                        if cmd[1].replace(" ", "") == "":
                            raise IndexError
                        self._command_unadmin(cmd[1])
                    case "/ban":
                        if cmd[1].replace(" ", "") == "":
                            raise IndexError
                        self._command_ban(cmd[1], None)
                    case "/unban":
                        if cmd[1].replace(" ", "") == "":
                            raise IndexError
                        self._command_unban(cmd[1], None)
                    case "/list":
                        if cmd[1].replace(" ", "") == "":
                            raise IndexError
                        self._command_list(cmd[1], None)
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
        exit(0)

    def _receive_connection(self):
        e, n = self.__rsa_client.public_key()
        while self.__running:
            try:
                client, address = self.__server.accept()
                init_data = client.recv(1024).decode("utf-8").split("$$$$")
                client.send("{}$$$${}".format(e, n).encode("utf-8"))
                if address[0] in self.__banned_ips_list:
                    raise BannedUserIp
                if init_data[0] in self.__banned_nicknames_list:
                    raise BannedUserNickname
                if init_data[0] in self.__clients_nicknames_list:
                    raise NicknameAlreadyTaken
                self.__clients_list.append(client)
                self.__clients_nicknames_list.append(init_data[0])
                self.__clients_codes_list.append(
                    (int(init_data[1]), int(init_data[2])))
                self.__clients_threads_list.append(StoppableThread(
                    target=self._handle_client, args=(client, )))
                self.__clients_threads_list[-1].start()
                self._broadcast(
                    ">INFO<: User {} has join the chat.".format(init_data[0]), client)
                self._print_system_information(
                    "User '{}' connected from '{}'.".format(init_data[0], address[0]))
            except BannedUserIp:
                client.send(RSAImplementation.encrypt_msg_default(
                    ">BAN<: You are banned at this server.", int(init_data[1]), int(init_data[2])).encode("utf-8"))
                self._print_system_error_light(
                    "Connection from '{}' rejected. Address IP banned.".format(address[0]))
                client.close()
            except BannedUserNickname:
                client.send(RSAImplementation.encrypt_msg_default(
                    ">BAN<: Your nickname is banned at this server.", int(init_data[1]), int(init_data[2])).encode("utf-8"))
                self._print_system_error_light(
                    "Connection from '{}' rejected. Nickname '{}' is banned.".format(address[0], init_data[0]))
                client.close()
            except NicknameAlreadyTaken:
                client.send(RSAImplementation.encrypt_msg_default(
                    ">ERROR<: This nickname is already taken. Choose another one.", int(init_data[1]), int(init_data[2])).encode("utf-8"))
                client.close()
            except (ValueError, IndexError, UnboundLocalError):
                if client and address:
                    self._print_system_error(
                        "Incorrect data from '{}', connection denied. More client info: {}.".format(address[0], client))
                    self._close_connection(client)
            except (ConnectionError, ConnectionResetError, ConnectionAbortedError):
                self._print_system_error(
                    "Connection from '{}' canceled. Connection error.".format(address[0]))
                self._close_connection(client)
            except OSError:
                if self.__running:
                    self._stop()
                break

    def _handle_client(self, client):
        nickname = self.__clients_nicknames_list[self.__clients_list.index(
            client)]
        while self.__running:
            try:
                message = self.__rsa_client.decrypt_msg(
                    client.recv(1024).decode("utf-8"))
                if message.startswith("/"):
                    message_command = message.split(" ")
                    match message_command[0]:
                        case "/kick":
                            if client not in self.__clients_admins_list:
                                raise UnauthorizedError
                            if message_command[1].replace(" ", "") == "":
                                raise IndexError
                            self._command_kick(message_command[1], client)
                        case "/ban":
                            if client not in self.__clients_admins_list:
                                raise UnauthorizedError
                            if message_command[1].replace(" ", "") == "":
                                raise IndexError
                            self._command_ban(message_command[1], client)
                        case "/unban":
                            if client not in self.__clients_admins_list:
                                raise UnauthorizedError
                            if message_command[1].replace(" ", "") == "":
                                raise IndexError
                            self._command_unban(message_command[1], client)
                        case "/list":
                            if message_command[1].replace(" ", "") == "":
                                raise IndexError
                            self._command_list(message_command[1], client)
                        case "/pv":
                            if message_command.__len__() < 3 or message_command[1].replace(" ", "") == "" or message_command[2].replace(" ", "") == "":
                                self._send_to(
                                    client, ">ERROR<: This command requires two parameters (/pv [nickname] [message]). Try again.")
                            else:
                                self._command_private_msg(
                                    nickname, message_command[1], message_command[2], client)
                        case _:
                            self._send_to(
                                client, ">ERROR<: Unknown command. Try again.")
                else:
                    self._broadcast("<{}>: {}".format(nickname, message), None)
            except UnauthorizedError:
                self._send_to(
                    client, ">ERROR<: This command requires admin permissions.")
            except IndexError:
                self._send_to(
                    client, ">ERROR<: This command requires parameter. Try again.")
            except (ConnectionError, ConnectionResetError, ConnectionAbortedError, OSError):
                if self.__running:
                    self._print_system_error(
                        "Connection with '{}' has been lost.".format(nickname))
                    self._close_connection(client)
                break

    def _send_to(self, to_client, message):
        if message == "":
            return
        try:
            e, n = self.__clients_codes_list[self.__clients_list.index(
                to_client)]
            to_client.send(RSAImplementation.encrypt_msg_default(
                message, e, n).encode("utf-8"))
        except ValueError:
            return
        except (ConnectionAbortedError, ConnectionResetError, ConnectionError):
            self._close_connection(to_client)

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
            except ValueError:
                continue
            except (ConnectionError, ConnectionResetError, ConnectionAbortedError):
                self._close_connection(client)

    def _close_connection(self, client):
        if client not in self.__clients_list:
            client.close()
            return
        index = self.__clients_list.index(client)
        nickname = self.__clients_nicknames_list[index]
        thread = self.__clients_threads_list[index]
        self.__clients_list.remove(client)
        self.__clients_nicknames_list.remove(nickname)
        self.__clients_codes_list.remove(self.__clients_codes_list[index])
        self.__clients_threads_list.remove(thread)
        if client in self.__clients_admins_list:
            self.__clients_admins_list.remove(client)
            self._broadcast(
                ">INFO<: Admin {} left the chat!".format(nickname), None)
            self._print_system_information(
                "Admin '{}' left the chat!".format(nickname))
        else:
            self._broadcast(
                ">INFO<: User {} left the chat!".format(nickname), None)
            self._print_system_information(
                "User '{}' left the chat!".format(nickname))
        client.close()
        thread.stop()

    def _stop(self):
        self._print_system_command("Stopping the server...")
        self.__running = False
        self.__receive_connection_thread.stop()
        while (self.__clients_list.__len__() > 0):
            for client in self.__clients_list:
                self._close_connection(client)
        self.__server.close()
        self._print_system_command("Server stopped.")

    def _command_msg(self, msg):
        msg = ">SERVER<: {}".format(msg)
        self._broadcast(msg, None)
        self._print_system_message(msg)

    def _command_private_msg(self, nickname_sender, nickname_to, message, client):
        if nickname_to == nickname_sender:
            self._send_to(
                client, ">ERROR<: You can not send private messages to yourself.")
            return
        try:
            self._send_to(self.__clients_list[self.__clients_nicknames_list.index(
                nickname_to)], "<{}> - <{}>: {}".format(nickname_sender, nickname_to, message))
            self._send_to(
                client, "<{}> - <{}>: {}".format(nickname_sender, nickname_to, message))
        except ValueError:
            self._send_to(
                client, ">ERROR<: The given nickname does not match any user. Try again.")

    def _command_kick(self, nickname, client=None):
        try:
            self._close_connection(
                self.__clients_list[self.__clients_nicknames_list.index(nickname)])
            self._broadcast(
                ">CMD<: {} has been kicked from the chat!".format(nickname), None)
        except ValueError:
            if client:
                self._send_to(
                    client, ">ERROR<: The given nickname does not match any user. Try again.")
            else:
                self._print_system_error(
                    "The given nickname does not match any user. Try again.")

    def _command_admin(self, nickname):
        try:
            self.__clients_admins_list.append(
                self.__clients_list[self.__clients_nicknames_list.index(nickname)])
            self._broadcast(
                ">CMD<: {} has been given admin permissions!".format(nickname), None)
            self._print_system_command(
                "'{}' has been given admin permissions!".format(nickname))
        except ValueError:
            self._print_system_error(
                "The given nickname does not match any user. Try again.")

    def _command_unadmin(self, nickname):
        try:
            self.__clients_admins_list.remove(
                self.__clients_list[self.__clients_nicknames_list.index(nickname)])
            self._broadcast(
                ">CMD<: {} has lost admin permissions!".format(nickname), None)
            self._print_system_command(
                "'{}' has lost admin permissions!".format(nickname))
        except ValueError:
            self._print_system_error(
                "The given nickname does not match any admin. Try again.")

    def _command_ban(self, nickname, client):
        try:
            client = self.__clients_list[self.__clients_nicknames_list.index(
                nickname)]
            self.__banned_nicknames_list.append(nickname)
            self.__banned_ips_list.append(client.getpeername()[0])
            self._send_to(client, ">BAN<: You were banned from the chat!")
            self._close_connection(client)
            self._broadcast(
                ">BAN<: {} has been banned from the chat!".format(nickname), None)
            self._print_system_error_light(
                "'{}' has been banned from the chat!".format(nickname))
        except ValueError:
            if client:
                self._send_to(
                    client, ">ERROR<: The given nickname does not match any user. Try again.")
            else:
                self._print_system_error(
                    "The given nickname does not match any user. Try again.")
    # tutaj

    def _command_unban(self, nickname, client):
        try:
            index = self.__banned_nicknames_list.index(nickname)
            self.__banned_nicknames_list.pop(index)
            self.__banned_ips_list.pop(index)
            self._broadcast(
                ">UNBAN<: {} has been unbanned from the chat!".format(nickname), None)
            self._print_system_information_light(
                "'{}' has been unbanned from the chat!".format(nickname))
        except ValueError:
            if client:
                self._send_to(
                    client, ">ERROR<: The given nickname does not match any user. Try again.")
            else:
                self._print_system_error(
                    "The given nickname does not match any user. Try again.")

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
                self._print_system_error("\nBanned users list:\n")
                for banned in self.__banned_nicknames_list:
                    self._print_system_error(banned+" ")  # zwykłe printy ?
            case _:
                self._print_system_command(
                    "The given parameter does not match any type. Try again.")

    def _command_help(self):
        self._print_system_command_light("/stop -> closes server")
        self._print_system_command("/clear -> clears console")
        self._print_system_command_light(
            "/msg [message] -> sends server message to all")
        self._print_system_command(
            "/kick [nickname] -> kicks user from server")
        self._print_system_command_light(
            "/admin [nickname] -> gives user admin permissions")
        self._print_system_command("/help -> prints commands informations")
    # tutaj

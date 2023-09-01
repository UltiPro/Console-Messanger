import os
import socket
import re
from threading import Thread

from chat.app import ConsoleMessanger
from rsa.rsa import RSA


class ClientConsoleMessanger(ConsoleMessanger):
    def __init__(self, nickname="User", server_address="127.0.0.1", server_port=50500):
        self.__nickname = nickname
        self.__server_address = server_address
        self.__server_port = server_port
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__rsa_client = RSA()
        self.__receive_messages_thread = None
        self.__server_public_key_e = None
        self.__server_public_key_n = None
        self.__running = True
        self.__quit_by_button = False

    def start(self):
        self._clear_console()
        self._print_system_information("Connecting to server at {}:{}, your nickname: {}.".format(
            self.__server_address, self.__server_port, self.__nickname))
        try:
            self.__client.connect((self.__server_address, self.__server_port))
            self.__client.send("{}$$$${}$$$${}".format(self.__nickname, self.__rsa_client.public_key()[
                               0], self.__rsa_client.public_key()[1]).encode("utf-8"))
            self.__server_public_key_e, self.__server_public_key_n = self.__client.recv(
                65536).decode("utf-8").split("$$$$")
            self.__server_public_key_e = int(self.__server_public_key_e)
            self.__server_public_key_n = int(self.__server_public_key_n)
        except:
            self._print_system_error(
                "Connection error or internal server error. Stopping client...")
            return
        self.__receive_messages_thread = Thread(target=self.__receive_messages)
        self.__receive_messages_thread.start()
        while self.__running:
            try:
                message = input()
                if not self.__running:
                    break
                if len(message) < 1:
                    self._print_system_error(
                        "Empty input. Type command or message: (Type /help for more informations)")
                    continue
                if len(message) > 128:
                    self._print_system_error(
                        "Message cannot be longer than 128 characters.")
                    continue
                if message.startswith("/"):
                   self.__commands(message)
                   continue
                self.__client.send(RSA.encrypt_msg_default(
                    message, self.__server_public_key_e, self.__server_public_key_n).encode("utf-8"))
            except KeyboardInterrupt:
                if not self.__quit_by_button:
                    self.__stop()
                break
            except:
                self._print_system_error(
                    "Connection error or internal server error. Stopping client...")
                self.__stop()
                break
        os._exit(0)

    def __receive_messages(self):
        while self.__running:
            try:
                message = self.__rsa_client.decrypt_msg(
                    self.__client.recv(65536).decode("utf-8"))
            except:
                if self.__running:
                    self._print_system_error("Connection terminated.")
                    self.__stop()
                    self.__quit_by_button = True
                    self._print_system_command("Press enter to exit...")
                break
            if message == "":
                continue
            elif message.startswith(">INFO<:"):
                self._print_system_information(message)
            elif message.startswith(">CMD<:"):
                self._print_system_command(message)
            elif message.startswith(">ERROR<:"):
                self._print_system_error(message)
            elif message.startswith(">BAN<:"):
                self._print_system_ban(message)
            elif message.startswith(">UNBAN<:"):
                self._print_system_unban(message)
            elif message.startswith(">SERVER<:"):
                self._print_system_server_message(message)
            elif re.match("^<\w*> - <\w*>: .*$", message):
                self._print_system_private_message(message)
            else:
                print(message)

    def __stop(self):
        self._print_system_command("Stopping the client...")
        self.__running = False
        self.__client.close()
        self._print_system_command("Client stopped.")

    def __commands(self, command):
        match command:
            case "/stop":
                self.__stop()
            case "/clear":
                self._clear_console()
                self._print_system_command("Console cleared...")
            case "/help":
                self.__help()
            case _:
                self.__client.send(RSA.encrypt_msg_default(
                    command, self.__server_public_key_e, self.__server_public_key_n).encode("utf-8"))

    def __help(self):
        self._print_system_command("\n/stop -> closes application")
        self._print_system_command2("/clear -> clears console")
        self._print_system_command(
            "/pv [nickname] [message] send a private message to the specified user")
        self._print_system_command2(
            "/kick [nickname] -> kicks user from server (requires admin permissions)")
        self._print_system_command(
            "/ban [nickname] -> bans user from server (requires admin permissions)")
        self._print_system_command2(
            "/unban [nickname] -> unbans user from server (requires admin permissions)")
        self._print_system_command("/list u -> prints list of connected users")
        self._print_system_command2(
            "/list a -> prints list of connected users with admin permissions")
        self._print_system_command("/list b -> prints list of banned users")
        self._print_system_command2("/help -> prints commands informations\n")

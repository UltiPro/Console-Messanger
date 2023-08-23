import socket
import re

from main.app import ConsoleMessanger
from thread.stoppableThread import StoppableThread
from rsa.rsaImplementation import RSAImplementation


class ClientConsoleMessanger(ConsoleMessanger):
    def __init__(self, nickname="User", server_address="127.0.0.1", server_port=50500):
        self.__nickname = nickname
        self.__server_address = server_address
        self.__server_port = server_port
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__rsa_client = RSAImplementation()
        self.__receive_messages_thread = None
        self.__server_public_key_e = None
        self.__server_public_key_n = None
        self.__running = True

    def start(self):
        self._clear_console()
        self._print_system_information("Connecting to server at {}:{}, your nickname: {}.".format(
            self.__server_address, self.__server_port, self.__nickname))
        try:
            self.__client.connect((self.__server_address, self.__server_port))
            self.__client.send("{}$$$${}$$$${}".format(self.__nickname, self.__rsa_client.public_key()[
                               0], self.__rsa_client.public_key()[1]).encode("utf-8"))
            self.__server_public_key_e, self.__server_public_key_n = self.__client.recv(
                1024).decode("utf-8").split("$$$$")
            self.__server_public_key_e = int(self.__server_public_key_e)
            self.__server_public_key_n = int(self.__server_public_key_n)
        except:
            #tutaj
            self._print_system_error(
                "Server internal error. Stopping client...")
            #tutaj
            return
        self.__receive_messages_thread = StoppableThread(
            target=self._receive_messages)
        self.__receive_messages_thread.start()
        while self.__running:
            try:
                # tutaj
                message = input("Type command or message: (Type /help for more informations)\n")
                if len(message) == 0:
                    continue
                if message.startswith("/"):
                   self._commands(message)
                   continue
                self.__client.send(RSAImplementation.encrypt_msg_default(
                    message, self.__server_public_key_e, self.__server_public_key_n).encode("utf-8"))
            except (ConnectionError, ConnectionResetError):
                self._print_system_error(
                    "Connection to server terminated. Press any button to stop client...")
                self.__running = False
                break
            except EOFError:
                self._print_system_error("Ctrl + C -> Stopping client...")
                self._stop()
            except KeyboardInterrupt:
                self._stop()
                break
            # tutaj
        exit(0)

    def _receive_messages(self):
        while self.__running:
            try:
                message = self.__rsa_client.decrypt_msg(
                    self.__client.recv(1024).decode("utf-8"))
                # tutaj
            except (ConnectionError, ConnectionResetError):
                if not self.__receive_messages_thread.stopped():
                    self._print_system_error(
                        "Connection error. Press any button to stop client...")
                    self.__running = False
                break
            if message == "":
                continue
            elif message.startswith(">INFO<:"):
                self._print_system_information(message)
            elif message.startswith(">UNBAN<:"):
                self._print_system_information_light(message)
            elif message.startswith(">CMD<:"):
                self._print_system_command(message)
            elif message.startswith(">ERROR<:"):
                self._print_system_error(message)
            elif message.startswith(">BAN<:"):
                self._print_system_error_light(message)
            elif message.startswith(">SERVER<:"):
                self._print_system_server_message(message)
            elif re.match("^<\w*> - <\w*>: .*$", message):
                self._print_system_private_message(message)
            else:
                print(message)
                # tutaj

    def _stop(self):
        self._print_system_command("Stopping the client...")
        self.__running = False
        self.__receive_messages_thread.stop()
        self.__client.close()
        self._print_system_command("Client stopped.")

    def _commands(self, cmd):
        match cmd:
            case "/stop":
                self._stop()
            case "/clear":
                self._clear_console()
                self._print_system_command("Console cleared...")
            case "/help":
                self._help()
            case _:
                self.__client.send(RSAImplementation.encrypt_msg_default(
                    cmd, self.__server_public_key_e, self.__server_public_key_n).encode("utf-8"))

    def _help(self):
        self._print_system_command_light("\n/stop -> closes application")
        self._print_system_command("/clear -> clears console")
        self._print_system_command_light(
            "/kick [nickname] -> kicks user from server (requires admin permissions)")
        self._print_system_command(
            "/ban [nickname] -> bans user from server (requires admin permissions)")
        self._print_system_command_light(
            "/unban [nickname] -> unbans user from server (requires admin permissions)")
        self._print_system_command("/list u -> prints list of connected users")
        self._print_system_command_light(
            "/list a -> prints list of connected users with admin permissions")
        self._print_system_command("/list b -> prints list of banned users")
        self._print_system_command_light(
            "/help -> prints commands informations\n")

import socket

from main.app import ConsoleMessanger
from thread.stoppableThread import StoppableThread
from rsa.rsaImplementation import RSAImplementation


class ClientConsoleMessanger(ConsoleMessanger):
    def __init__(self, nickname="Undefined", server_address="127.0.0.1", server_port=50500):
        super()
        self.__server_address = server_address
        self.__server_port = server_port
        self.__nickname = nickname
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__rsa_client = RSAImplementation()
        self.__server_public_key_e = None
        self.__server_public_key_n = None
        self.__recive_theard = None
        self.__write_theard = None
        self.__running = True

    def start(self):
        self._console_clear()
        self._print_system_info("Connecting to server at {}:{}, nickname: {}".format(
            self.__server_address, self.__server_port, self.__nickname))
        try:
            self.__client.connect((self.__server_address, self.__server_port))
            e, n = self.__rsa_client.public_key()
            self.__client.send("{}$$$${}$$$${}".format(
                self.__nickname, e, n).encode("utf-8"))
            self.__server_public_key_e, self.__server_public_key_n = self.__client.recv(
                1024).decode("utf-8").split("$$$$")
            self.__server_public_key_e = int(self.__server_public_key_e)
            self.__server_public_key_n = int(self.__server_public_key_n)
        except (ConnectionRefusedError, ConnectionResetError, TimeoutError):
            self._print_system_error(
                "Could not resolve server. Stopping client...")
            return

        self.__recive_theard = StoppableThread(target=self._recive)
        self.__recive_theard.start()

        self.__write_theard = StoppableThread(target=self._write)
        self.__write_theard.start()

    def _recive(self):
        while self.__running:
            try:
                message = self.__rsa_client.decrypt_msg(
                    self.__client.recv(1024).decode("utf-8"))
            except (ConnectionError, ConnectionResetError):
                if not self.__recive_theard.stopped():
                    self._print_system_error(
                        "Connection error. Press any button to stop client...")
                    self.__running = False
                break
            if message.startswith("Info: "):
                self._print_system_comunication(message)
            else:
                print(message)

    def _write(self):
        while self.__running:
            try:
                message_input = input()
                if len(message_input) == 0:
                    continue
                if message_input.startswith("/"):
                    self._commands_pallete(message_input)
                    continue
                message = "<{}>: {}".format(self.__nickname, message_input)
                self.__client.send(RSAImplementation.encrypt_msg_default(
                    message, self.__server_public_key_e, self.__server_public_key_n).encode("utf-8"))
            except (ConnectionError, ConnectionResetError):
                if not self.__write_theard.stopped():
                    self._print_system_error(
                        "Connection to server terminated. Press any button to stop client...")
                    self.__running = False
                break
            except EOFError:
                self._print_system_error("Ctrl + C -> Stopping client...")
                self._stop()

    def _commands_pallete(self, cmd):
        match cmd:
            case "/client-stop":
                self._print_system_info("Client Stopped.")
                self._stop()
            case "/client-clear":
                self._console_clear()
                self._print_system_info("Console cleared...")
            case _:
                self._print_system_error("Unknown command. Try again.")

    def _stop(self):
        self.__recive_theard.stop()
        self.__write_theard.stop()
        self.__client.close()
        exit(0)

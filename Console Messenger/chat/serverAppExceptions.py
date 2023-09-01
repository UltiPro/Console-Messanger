class BannedUserIp(Exception):
    __message = ">BAN<: You are banned at this server."

    def get_message(self):
        return self.__message


class BannedUserNickname(Exception):
    __message = ">BAN<: Your nickname is banned at this server."

    def get_message(self):
        return self.__message


class NicknameAlreadyTaken(Exception):
    __message = ">ERROR<: This nickname is already taken. Choose another one."

    def get_message(self):
        return self.__message


class NicknameTooShortTooLong(Exception):
    __message = ">ERROR<: Nickname cannot be longer than 24 characters and shorter than 3 characters."

    def get_message(self):
        return self.__message


class UnauthorizedUserAccess(Exception):
    __message = ">ERROR<: This command requires admin permissions."

    def get_message(self):
        return self.__message

import math
import random


class RSA():
    def __init__(self, min=2, max=101):
        self.__n, self.__phi = self._generate_n_phi(min, max)
        self.__e = self._generate_e()
        self.__d = self._generate_d()

    def _generate_n_phi(self, min, max):
        numbers = [i for i in range(min, max)]
        for i in range(min, max):
            for j in range(2, math.ceil(i/2)):
                if i % j == 0:
                    numbers.remove(i)
                    break
        p = random.choice(numbers)
        numbers.remove(p)
        q = random.choice(numbers)
        return (p * q, (p - 1) * (q - 1))

    def _generate_e(self):
        e_values = []
        for i in range(2, self.__phi):
            if math.gcd(i, self.__phi) == 1:
                e_values.append(i)
        return random.choice(e_values)

    def _generate_d(self):
        for i in range(2, self.__phi):
            if (i * self.__e) % self.__phi == 1:
                return i

    def public_key(self):
        return self.__e, self.__n

    def _encrypt_char(self, char):
        if type(char) == str:
            char = ord(char)
        return pow(char, self.__e) % self.__n

    def _decrypt_char(self, char):
        return chr(pow(int(char), self.__d) % self.__n)

    def encrypt_msg(self, msg):
        return_msg = ""
        for char in msg:
            return_msg += "{}%$%".format(self._encrypt_char(char))
        return return_msg

    def decrypt_msg(self, msg):
        return_msg = ""
        for char in msg.split("%$%")[0:-1]:
            return_msg += self._decrypt_char(char)
        return return_msg

    @staticmethod
    def encrypt_char_default(char, e, n):
        if type(char) == str:
            char = ord(char)
        return pow(char, e) % n

    @staticmethod
    def encrypt_msg_default(msg, e, n):
        return_msg = ""
        for char in msg:
            return_msg += "{}%$%".format(RSA.encrypt_char_default(char, e, n))
        return return_msg

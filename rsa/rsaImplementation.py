import random
import math


class RSAImplementation():
    def __init__(self):
        self._n, self._phi = self._generate_n_phi()
        self._e = self._generate_e()
        self._d = self._generate_d()

    def _generate_n_phi(self):
        numbers = [i for i in range(2, 101)]
        for i in range(2, 101):
            for j in range(2, math.ceil(i/2)+1):
                if i % j == 0:
                    numbers.remove(i)
                    break
                else:
                    continue
        p = random.choice(numbers)
        numbers.remove(p)
        q = random.choice(numbers)
        return (p * q, (p - 1) * (q - 1))

    def _generate_e(self):
        e_values = []
        for i in range(2, self._phi):
            if math.gcd(i, self._phi) == 1:
                e = i
                e_values.append(e)
        return random.choice(e_values)

    def _generate_d(self):
        for i in range(2, self._phi):
            if (i * self._e) % self._phi == 1:
                d = i
                break
        return d

    def public_key(self):
        return self._e, self._n

    def _encrypt_char(self, char):
        c = pow(ord(char), self._e) % self._n
        return c

    def _decrypt_char(self, char):
        p = pow(int(char), self._d) % self._n
        return chr(p)

    def encrypt_msg(self, msg):
        return_msg = ""
        for e in msg:
            return_msg += "{}%$%".format(self._encrypt_char(e))
        return return_msg

    def decrypt_msg(self, msg):
        return_msg = ''
        for e in msg.split("%$%")[0:-1]:
            return_msg += self._decrypt_char(e)
        return return_msg

    @staticmethod
    def encrypt_char_default(char, e, n):
        c = pow(ord(char), e) % n
        return c

    @staticmethod
    def encrypt_msg_default(msg, e, n):
        return_msg = ""
        for elem in msg:
            return_msg += "{}%$%".format(
                RSAImplementation.encrypt_char_default(elem, e, n))
        return return_msg

import sympy


class RSA():
    __bit_length = 1024
    __block_size = __bit_length // 8

    def __init__(self):
        self.__n, self.__e, self.__d = self.__generate_keypair()

    def __generate_keypair(self):
        p = sympy.randprime(2**(self.__bit_length//2), 2 **
                            (self.__bit_length//2 + 1))
        q = sympy.randprime(2**(self.__bit_length//2), 2 **
                            (self.__bit_length//2 + 1))
        n = p * q
        phi = (p - 1) * (q - 1)
        e = sympy.randprime(2, phi)
        return n, e, sympy.mod_inverse(e, phi)

    def __mod_exp(self, base, exponent):
        result = 1
        base = base % self.__n
        while exponent > 0:
            if exponent % 2 == 1:
                result = (result * base) % self.__n
            exponent >>= 1
            base = (base * base) % self.__n
        return result

    def __encrypt_block(self, block):
        return self.__mod_exp(int.from_bytes(block.encode('utf-8'), byteorder='big'), self.__e)

    def __decrypt_block(self, encrypted_block):
        decrypted_num = self.__mod_exp(encrypted_block, self.__d)
        return decrypted_num.to_bytes((decrypted_num.bit_length() + 7) // 8, byteorder='big').decode('utf-8')

    def encrypt_msg(self, message):
        blocks = [message[i:i+self.__block_size]
                  for i in range(0, len(message), self.__block_size)]
        return " ".join([str(self.__encrypt_block(block)) for block in blocks])

    def decrypt_msg(self, encrypted_message):
        return ''.join([self.__decrypt_block(int(encrypted_block)) for encrypted_block in encrypted_message.split(" ")])

    def public_key(self):
        return self.__e, self.__n

    @staticmethod
    def __mod_exp_default(base, exponent, modulus):
        result = 1
        base = base % modulus
        while exponent > 0:
            if exponent % 2 == 1:
                result = (result * base) % modulus
            exponent >>= 1
            base = (base * base) % modulus
        return result

    @staticmethod
    def __encrypt_block_default(block, e, n):
        return RSA.__mod_exp_default(int.from_bytes(block.encode('utf-8'), byteorder='big'), e, n)

    @staticmethod
    def encrypt_msg_default(message, e, n):
        blocks = [message[i:i+RSA.__block_size]
                  for i in range(0, len(message), RSA.__block_size)]
        return " ".join([str(RSA.__encrypt_block_default(block, e, n)) for block in blocks])

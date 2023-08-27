import sympy


class RSA():
    bit_length = 1024
    block_size = bit_length // 8

    def __init__(self):
        self.__n, self.__e, self.__d = self._generate_keypair()

    def _generate_keypair(self):
        p = sympy.randprime(2**(RSA.bit_length//2), 2 **
                            (RSA.bit_length//2 + 1))
        q = sympy.randprime(2**(RSA.bit_length//2), 2 **
                            (RSA.bit_length//2 + 1))
        n = p * q
        phi = (p - 1) * (q - 1)
        e = sympy.randprime(2, phi)
        return n, e, sympy.mod_inverse(e, phi)

    def _mod_exp(self, base, exponent):
        result = 1
        base = base % self.__n
        while exponent > 0:
            if exponent % 2 == 1:
                result = (result * base) % self.__n
            exponent >>= 1
            base = (base * base) % self.__n
        return result

    def _encrypt_block(self, block):
        return self._mod_exp(int.from_bytes(block.encode('utf-8'), byteorder='big'), self.__e)

    def _decrypt_block(self, encrypted_block):
        decrypted_num = self._mod_exp(encrypted_block, self.__d)
        return decrypted_num.to_bytes((decrypted_num.bit_length() + 7) // 8, byteorder='big').decode('utf-8')

    def encrypt_msg(self, message):
        blocks = [message[i:i+RSA.block_size]
                  for i in range(0, len(message), RSA.block_size)]
        return " ".join([str(self._encrypt_block(block)) for block in blocks])

    def decrypt_msg(self, encrypted_message):
        return ''.join([self._decrypt_block(int(encrypted_block)) for encrypted_block in encrypted_message.split(" ")])

    def public_key(self):
        return self.__e, self.__n

    @staticmethod
    def mod_exp(base, exponent, modulus):
        result = 1
        base = base % modulus
        while exponent > 0:
            if exponent % 2 == 1:
                result = (result * base) % modulus
            exponent >>= 1
            base = (base * base) % modulus
        return result

    @staticmethod
    def encrypt_block(block, e, n):
        return RSA.mod_exp(int.from_bytes(block.encode('utf-8'), byteorder='big'), e, n)

    @staticmethod
    def encrypt_msg_default(message, e, n):
        blocks = [message[i:i+RSA.block_size]
                  for i in range(0, len(message), RSA.block_size)]
        return " ".join([str(RSA.encrypt_block(block, e, n)) for block in blocks])

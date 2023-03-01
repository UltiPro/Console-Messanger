import random
import math


class RSAImplementation():
    @staticmethod
    def rsa_generate_keys(p, q):
        n = p * q
        phi_n = (p-1) * (q-1)
        e = random.randint(2, phi_n - 1)
        while math.gcd(e, phi_n) != 1:
            e = random.randint(2, phi_n - 1)
        d = pow(e, -1, phi_n) # może być źle
        #modular_inverse(e, phi_n)
        return ((p, q, d), (n, e))

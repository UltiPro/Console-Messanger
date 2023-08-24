from rsa import RSA

rsa = RSA()

message = "Example test text"

print("Original message: {}".format(message))

encrypted_message = rsa.encrypt_msg(message)

print("Encrypted message: {}".format(encrypted_message))

print("Decrypted message: {}".format(rsa.decrypt_msg(encrypted_message)))

from rsaImplementation import RSAImplementation

rsa_implementation = RSAImplementation()

msg = "Example test text"

encrypted_message = rsa_implementation.encrypt_msg(msg)

print(encrypted_message)

decrypted_message = rsa_implementation.decrypt_msg(encrypted_message)

print(decrypted_message)

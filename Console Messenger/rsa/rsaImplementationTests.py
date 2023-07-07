from rsaImplementation import RSAImplementation

rsaImplementation = RSAImplementation()

msg = "Example test text"

encrypted_message = rsaImplementation.encrypt_msg(msg)

print(encrypted_message)

decrypted_message = rsaImplementation.decrypt_msg(encrypted_message)

print(decrypted_message)

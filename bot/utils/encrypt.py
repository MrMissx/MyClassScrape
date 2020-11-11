from bot import ENC_SEC, DEC_SEC

#decryption Key
decrypted = DEC_SEC.encode()
#encryption Key
encrypted = ENC_SEC.encode()


def encrypt(msg):
    encrypt_table = bytes.maketrans(decrypted, encrypted)
    result = msg.translate(encrypt_table)
    return result


def decrypt(msg):
    decrypt_table = bytes.maketrans(encrypted, decrypted)
    result = msg.translate(decrypt_table)
    return result


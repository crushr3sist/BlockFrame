import random

import cryptography
from cryptography.fernet import Fernet


def generate_random_file():
    with open("random.txt", "wb") as f:
        for _ in range(1024 * 1024):
            f.write(random.randbytes(8))


def encrypt(filename: str, key: str):
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()

    encrypted_data = f.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)


def decrypt(filename: str, key: bytes):
    f = Fernet(key)

    with open(filename, "rb") as file:
        encrypted_data = file.read()

    try:
        decrypted_data = f.decrypt(encrypted_data)
    except cryptography.fernet.InvalidToken:
        return

    with open(filename, "wb") as file:
        file.write(decrypted_data)




if __name__ == "__main__":
    generate_random_file()
    # key = base64.urlsafe_b64encode(hashlib.sha256(b"password").digest())

    # decrypt("random.txt", key)
    # encrypt("random.txt", key)

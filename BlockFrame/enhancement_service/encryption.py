from cryptography.fernet import Fernet
import cryptography
from ..database_service.defaultmodel import ChunkHashes, DefaultChunkModel


class Encryption:
    def __init__(self, *args, **kwargs) -> None:
        self.config = kwargs.get("config")
        self.path = self.config["file-storage-path"]
        self.db = kwargs.get("db")
        if (
            "enhancement-settings" in self.config
            and "secret_key" in self.config["enhancement-settings"]
        ):
            self.secret_key = self.config["enhancement-settings"]["secret_key"]
        else:
            self.secret_key = self.generate_key()

    def generate_key(self):
        return Fernet.generate_key()

    def get_key(self):
        return self.secret_key

    def apply_encryption(self, file_bytes, secret_key):
        f = Fernet(secret_key)
        try:
            encrypted_data = f.encrypt(file_bytes)
            return encrypted_data
        except Exception as e:
            raise e


class Decryption:
    def __init__(self, *args, **kwargs) -> None:
        self.config = kwargs.get("config")
        self.path = self.config["file-storage-path"]
        self.db = kwargs.get("db")

    def decrypt(self, encrypted_data, secret_key):
        print(secret_key)

        f = Fernet(secret_key)
        try:
            decrypted_data = f.decrypt(encrypted_data)
            return decrypted_data
        except Exception as e:
            raise e


class EncryptionController:
    def __init__(self, *args, **kwargs) -> None:
        self.config = kwargs.get("config")
        self.db = kwargs.get("db")

    def generate_key(self):
        return Fernet.generate_key()

    def get_encryption_method(self):
        return Encryption(config=self.config, db=self.db)

    def apply_encryption(self, file_bytes, secret_key):
        encryption = self.get_encryption_method()
        return encryption.apply_encryption(file_bytes, secret_key)

    def apply_decryption(self, encrypted_data, secret_key):
        decryption = Decryption(config=self.config, db=self.db)
        return decryption.decrypt(encrypted_data, secret_key)

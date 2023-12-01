<<<<<<< HEAD
from cryptography.fernet import Fernet
=======
import cryptography
from cryptography.fernet import Fernet
from ..database_service.defaultmodel import ChunkHashes, DefaultChunkModel
>>>>>>> af2468f5c26fdd73fdd88b22780e5049c62444e1


class Encryption:
    def __init__(self, *args, **kwargs) -> None:
<<<<<<< HEAD
        self.config = kwargs.get("config")
        self.path = self.config["file-storage-path"]
        self.db = kwargs.get("db")
        if self.config["enhancement-settings"]["secret_key"] != None:
            self.secret_key = self.config["enhancement-settings"]["secret_key"]
        else:
            self.secret_key = self.generate_key()

    def generate_key(self):
        return Fernet.generate_key()

    def apply_encryption(self, file_bytes):
        f = Fernet(self.secret_key)
        encrypted_data = f.encrypt(file_bytes)
        return encrypted_data
=======
        ...
>>>>>>> af2468f5c26fdd73fdd88b22780e5049c62444e1

    def apply_encryption(self, file_bytes, file_key) -> bytes:
        f = Fernet(file_key)
        return f.encrypt(file_bytes)

    def apply_decrypt(self, file_bytes, file_key) -> bytes:
        f = Fernet(file_key)
        return f.decrypt(file_bytes)

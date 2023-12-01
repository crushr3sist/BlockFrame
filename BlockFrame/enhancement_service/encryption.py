from cryptography.fernet import Fernet
import cryptography
from ..database_service.defaultmodel import ChunkHashes, DefaultChunkModel


class Encryption:
    def __init__(self, *args, **kwargs) -> None:
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

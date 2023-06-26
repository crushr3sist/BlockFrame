from ..database_service.defaultmodel import DefaultChunkModel


class Encryption:
    def __init__(self, *args, **kwargs) -> None:
        self.config = kwargs.get("config")
        self.path = self.config["file-storage-path"]
        self.db = kwargs.get("db")

    def apply_encryption(self):
        ...

    def save_compression_signature(self):
        ...


class Decryption:
    def __init__(self, *args, **kwargs) -> None:
        self.config = kwargs.get("config")
        self.path = self.config["file-storage-path"]
        self.db = kwargs.get("db")

    def decrypt(self):
        ...


class EncryptionController:
    ...

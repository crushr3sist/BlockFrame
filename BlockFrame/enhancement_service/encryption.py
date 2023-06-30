import cryptography
from cryptography.fernet import Fernet
from ..database_service.defaultmodel import ChunkHashes, DefaultChunkModel


class Encryption:
    def __init__(self, *args, **kwargs) -> None:
        ...

    def apply_encryption(self, file_bytes, file_key) -> bytes:
        f = Fernet(file_key)
        return f.encrypt(file_bytes)

    def apply_decrypt(self, file_bytes, file_key) -> bytes:
        f = Fernet(file_key)
        return f.decrypt(file_bytes)

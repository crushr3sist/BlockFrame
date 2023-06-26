from BlockFrame.enhancement_service.compression import CompressionController
from BlockFrame.enhancement_service.encryption import EncryptionController
from BlockFrame.enhancement_service.integrity import IntegrityController
from BlockFrame.enhancement_service.metadata import MetadataController
from BlockFrame.enhancement_service.vectorised_search import SearchController


class Enhancements:
    def __init__(self, *args, **kwargs):
        self.config = kwargs.get("config")
        self.db = kwargs.get("db")

        self.compression = CompressionController()
        self.encryption = EncryptionController()
        self.integrity = IntegrityController()
        self.metadata = MetadataController()
        self.search = SearchController()

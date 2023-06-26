from BlockFrame.enhancement_service.compression import CompressionController
from BlockFrame.enhancement_service.encryption import EncryptionController
from BlockFrame.enhancement_service.integrity import IntegrityController
from BlockFrame.enhancement_service.metadata import MetadataController
from BlockFrame.enhancement_service.vectorised_search import SearchController


class Enhancements:
    def __init__(self, *args, **kwargs):
        self.config = kwargs.get("config")
        self.db = kwargs.get("db")

        self.compression = CompressionController(config=self.config, db=self.db)
        self.encryption = EncryptionController(config=self.config, db=self.db)
        self.integrity = IntegrityController(config=self.config, db=self.db)
        self.metadata = MetadataController(config=self.config, db=self.db)
        self.search = SearchController(config=self.config, db=self.db)

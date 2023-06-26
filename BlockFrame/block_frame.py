from typing import Literal, Union

from BlockFrame.chunking_service.chunking import ChunkHandler
from BlockFrame.chunking_service.config import Config
from BlockFrame.chunking_service.fetcher import Fetcher
from BlockFrame.database_service.database import BlockFrameDatabase
from BlockFrame.enhancement_service.enhancements import Enhancements


class BlockFrame:
    def __init__(
        self,
        config: str,
        option: Union[
            Literal["generic"], Literal["time"], Literal["secure"], Literal["custom"]
        ],
        encryption_key: str | bytes,
        encryption_algorithm: Union[Literal["Fernet"], Literal["RSA"], Literal["AES"]],
        compression_algorithm,
    ):
        self.config = Config(config)
        if config.config_id["encrypt"] == True and isinstance(encryption_key, None):
            raise Exception(
                "Config has encryption enabled, please provide encryption key"
            )

        self.database = BlockFrameDatabase(db_config=self.config.config_id)
        self.enhancements = Enhancements(config=self.config, db=self.database)
        self.chunker = ChunkHandler(
            db=self.database.get_db(),
            config=self.config.config_id,
            option=option,
            enhancements=self.enhancements,
        )
        self.fetcher = Fetcher(
            config=self.config.config_id,
            db=self.database.get_db(),
            enhancements=self.enhancements,
        )

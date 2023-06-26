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
        encryption_key: str | bytes | None = None,
    ):  # sourcery skip: raise-specific-error
        self.config = Config(config)
        if (
            self.config.config_id["enhancements"]["encrypt"] is True
            and encryption_key is None
        ):
            raise ValueError(
                "Config has encryption enabled, please provide encryption key"
            )

        self.database = BlockFrameDatabase(db_config=self.config.config_id)
        self.enhancements = Enhancements(config=self.config.config_id, db=self.database)
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

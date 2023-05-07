import hashlib
import os
import pathlib
from typing import Literal, Union

from BlockFrame.chunking_service.chunking import ChunkHandler
from BlockFrame.chunking_service.fetcher import Fetcher

from BlockFrame.chunking_service.config import Config
from BlockFrame.database_service.database import BlockFrameDatabase
from BlockFrame.database_service.defaultmodel import DefaultChunkModel


class BlockFrame:
    def __init__(
        self,
        config: str,
        option: Union[
            Literal["generic"], Literal["time"], Literal["secure"], Literal["custom"]
        ],
    ):
        self.config = Config(config)

        self.database = BlockFrameDatabase(db_config=self.config.config_id)
        self.chunker = ChunkHandler(
            db=self.database.get_db(), config=self.config.config_id, option=option
        )
        self.fetcher = Fetcher(config=self.config.config_id, db=self.database.get_db())

from typing import Literal, Union

from BlockFrame.chunking_service.chunking import ChunkHandler
from BlockFrame.chunking_service.config import Config
from BlockFrame.chunking_service.fetcher import Fetcher
from BlockFrame.database_service.database import BlockFrameDatabase


class BlockFrame:
    def __init__(
        self,
        config: str,
        option: Union[
            Literal["generic"], Literal["time"], Literal["secure"], Literal["custom"]
        ],
    ):
        """
        This function initializes several objects including a Config object, a BlockFrameDatabase
        object, a ChunkHandler object, and a Fetcher object.

        :param config: A string representing the configuration file to be used
        :type config: str
        :param option: The "option" parameter is a string literal that specifies the type of chunking to
        be used by the ChunkHandler object. It can be one of the following values: "generic", "time",
        "secure", or "custom"
        :type option: Union[
                    Literal["generic"], Literal["time"], Literal["secure"], Literal["custom"]
                ]
        """
        self.config = Config(config)

        self.database = BlockFrameDatabase(db_config=self.config.config_id)
        self.chunker = ChunkHandler(
            db=self.database.get_db(), config=self.config.config_id, option=option
        )
        self.fetcher = Fetcher(config=self.config.config_id, db=self.database.get_db())

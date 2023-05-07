import contextlib
from BlockFrame.database_service.defaultmodel import DefaultChunkModel
from BlockFrame.database_service.getters import BlockFrameDatabaseGetters
from BlockFrame.database_service.initalisation import *


class BlockFrameDatabase(BlockFrameDatabaseGetters, BlockFrameDatabaseInit):
    def __init__(self, *args, **kwargs):
        self.class_model = (
            DefaultChunkModel
            if kwargs.get("class_model") is not None
            else kwargs.get("class_model")
        )
        self.config = kwargs.get("db_config")
        self.database_obj = None

        with contextlib.suppress(KeyError):
            if custom_uri := self.config["database"]["uri"]:
                DatabaseInterface.custom_uri(custom_uri)
                self.database_obj = self.get_db()

        if not self.database_obj:
            self.database_obj = self.get_db()

        super().__init__(
            class_model=self.class_model,
            database_obj=self.database_obj,
            config=self.config,
        )

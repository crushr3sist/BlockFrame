import math
import pathlib

from BlockFrame import block_frame

from BlockFrame.database_service.defaultmodel import DefaultChunkModel

config_path = pathlib.Path("./config.json").absolute()
block_frame = block_frame.BlockFrame(config_path, option="generic")

chunker = block_frame.chunker
fetcher = block_frame.fetcher
chunker_db = block_frame.database

chunker_db.create_table(DefaultChunkModel)

data = chunker_db.get_all()


chunker.target("image.jpg", size=5)


chunker.generic_chunking()

fetcher.target("image.jpg")

fetcher.fetch()

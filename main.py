import pathlib

from BlockFrame import block_frame

config_path = pathlib.Path("./config.json").absolute()
block_frame = block_frame.BlockFrame(config_path, option="generic")

chunker = block_frame.chunker
fetcher = block_frame.fetcher
chunker_db = block_frame.database


data = chunker_db.get_all()


chunker.target(file_name="image.jpg", size=5)


chunker.generic_chunking()

fetcher.target("image.jpg")

fetcher.fetch()

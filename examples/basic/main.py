import pathlib

from BlockFrame import block_frame

# initialize BlockFrame
config_path = pathlib.Path("./config.json").absolute()
block_frame = block_frame.BlockFrame(config_path, option="generic")


# chunking
block_frame.chunker.target(file_name="image.jpg", size=5)

block_frame.chunker.generic_chunking()


# fetcher
block_frame.fetcher.target("image.jpg")

block_frame.fetcher.fetch()

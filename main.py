import pathlib

from BlockFrame import block_frame

config_path = pathlib.Path("./config.json").absolute()
block_frame = block_frame.BlockFrame(config_path, option="generic")


try:
    block_frame.chunker.target(file_name="image.jpg", size=5)

    block_frame.chunker.apply()
except Exception as e:
    print(e)


try:
    block_frame.fetcher.target("image.jpg")

    block_frame.fetcher.fetch()
except Exception as e:
    print(e)

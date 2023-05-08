# BlockFrame

![alt text](https://i.imgur.com/GGHdpCe.png)

BlockFrame is a file chunking library designed to work as a data-store solution alongside web apps and software. It provides a simple and flexible way to store large files by breaking them into smaller chunks that can be easily managed and retrieved.

## Features

- Chunk files into smaller pieces of fixed or variable size
- Store chunks in a database or on disk, depending on your storage needs
- Fetch and reassemble original files from their chunks
- Highly configurable and customizable to suit specific needs
- Built with modern Python libraries like SQLAlchemy and cryptography for fast and secure file storage and retrieval
- Comprehensive documentation and tests to ensure reliability and correctness

## Installation

You can install BlockFrame using pip:

```sh
pip install BlockFrame
```

## Usage

Here's an example of how to use BlockFrame to chunk and store a file:

```py
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
```

# Collaboration Tips

- If you encounter any issues or have suggestions for improvement, please open an issue on GitHub.
- Pull requests are welcome! Please ensure that your code adheres to the project's coding standards and that tests are passing before submitting a pull request.
- If you want to contribute but don't know where to start, please check the project's issues page or open-source guide for guidance.

# Different Ways to Use the Code

## Modifying Chunking Algorithm

You can modify the BlockFrame class to use different chunking algorithms. For example, you can use a sliding window algorithm to chunk files into smaller pieces.

```py
class BlockFrame(
    config: str,
    option: Literal['generic', 'time', 'secure']
)

```

3 very useful chunking algorithms are provided by default:

## Modifying Storage Options

You can modify the storage options used in the BlockFrame class by modifying the database configuration defined in the config.json file. By default, BlockFrame uses SQLite to store chunks in a database. However, you can modify the uri field in the database section of the configuration file to use a different database management system, such as MongoDB.

```json
{
  "database": {
    "uri": "mongodb://localhost:27017/",
    "name": "my_database"
  }
}
```

## Useable with context managers

Using a context manager with BlockFrame makes it easy to properly manage and clean up resources after use. The context manager takes care of initializing and tearing down the necessary resources like the chunker, fetcher, and database.

With the with statement, you can create a block of code where the BlockFrame object is instantiated and used. When the block is exited, the context manager's **exit** method is called to ensure that the resources are properly cleaned up.

In the example provided, the chunker object is used to target the file image.jpg and set a chunk size of 5. The generic_chunking method is then called to generate the chunks for the file. The fetcher object is used to target the same file and fetch the previously generated chunks.

Using a context manager ensures that all necessary resources are properly initialized and cleaned up, even if an error occurs during execution.

```py
import pathlib
from BlockFrame import block_frame
from BlockFrame.database_service.defaultmodel import DefaultChunkModel

config_path = pathlib.Path("./config.json").absolute()

with block_frame.BlockFrame(config_path, option="generic") as bf:
    bf.chunker.target("image.jpg", size=5)
    bf.chunker.generic_chunking()
    bf.fetcher.target("image.jpg")
    bf.fetcher.fetch()
```

I hope this helps! Let me know if you have any further questions.

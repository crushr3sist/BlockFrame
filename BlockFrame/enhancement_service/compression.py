import glob
import re
from typing import Iterable
import lz4
import functools
import lzf
import zlib
import snappy
from ..database_service.defaultmodel import DefaultChunkModel


class Compression:
    def __init__(self, *args, **kwargs) -> None:
        self.file_bytes = kwargs.get("file_bytes")

    def lz4_compression(self):
        lz4.compress(self.file_bytes)

    def zlib_compression(self):
        zlib.compress(self.file_bytes)

    def lzf_compression(self):
        # lzf.compress(self.file_bytes)
        ...

    def snappy_compression(self):
        # snappy.compress(self.file_bytes)
        ...


class Decompression:
    def __init__(self, *args, **kwargs) -> None:
        self.file_bytes = kwargs.get("file_bytes")

    def lz4_decompression(self):
        ...

    def zlib_decompression(self):
        ...

    def lzf_decompression(self):
        # lzf.uncompress(self.file_bytes, len(self.file_bytes))
        ...

    def snappy_decompression(self):
        ...


class CompressionController(Compression, Decompression):
    def __init__(self, *args, **kwargs) -> None:
        """{
            "fast_compression": "lz4",\n
            "higher_compression": "zlib",\n
            "balanced: "snappy",\n
            "simple": "lzf",\n
        }
        """
        super().__init__()
        self.config = kwargs.get("config")
        self.path = self.config["file-storage-path"]
        self.db = kwargs.get("db")

    def apply_compression(self):
        ...

    def apply_decompression(self):
        ...

import functools
import zlib
<<<<<<< HEAD
=======

import lz4.frame
import lzf
import snappy
>>>>>>> af2468f5c26fdd73fdd88b22780e5049c62444e1


class ZlibCompression:
    def __init__(self, *args, **kwargs):
        ...

    @functools.lru_cache
    def compress(self, file_bytes):
        return zlib.compress(file_bytes, level=zlib.Z_BEST_COMPRESSION)

    @functools.lru_cache
    def decompress(self, file_bytes):
        return zlib.decompress(file_bytes)


class CompressionController:
    def __init__(self, *args, **kwargs) -> None:
        """
        1: fast_compression -> lz4
        2: higher_compression -> zlib
        3: balanced -> snappy
        4: simple -> lzf
        """
        super().__init__()
        self.config = kwargs.get("config")

    def get_compression_method(self):
        return ZlibCompression()

    def apply_compression(self, file_bytes):
        return self.get_compression_method().compress(file_bytes=file_bytes)

    def apply_decompression(self, file_bytes):
        return self.get_compression_method().decompress(file_bytes=file_bytes)

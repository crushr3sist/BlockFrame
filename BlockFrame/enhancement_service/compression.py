import functools
import zlib
import lz4.frame
import lzf
import snappy


class CompressionBase:
    def compress(self):
        ...

    def decompress(self):
        ...


class Lz4Compression(CompressionBase):
    def __init__(self, *args, **kwargs):
        ...

    @functools.lru_cache
    def compress(self, file_bytes):
        return lz4.frame.compress(file_bytes)

    @functools.lru_cache
    def decompress(self, file_bytes):
        return lz4.frame.decompress(file_bytes)


class ZlibCompression(CompressionBase):
    def __init__(self, *args, **kwargs):
        ...

    @functools.lru_cache
    def compress(self, file_bytes):
        return zlib.compress(file_bytes, level=zlib.Z_BEST_COMPRESSION)

    @functools.lru_cache
    def decompress(self, file_bytes):
        return zlib.decompress(file_bytes)


class LzfCompression(CompressionBase):
    def __init__(self, *args, **kwargs):
        ...

    @functools.lru_cache
    def compress(self, file_bytes):
        return lzf.compress(self.file_bytes)

    @functools.lru_cache
    def decompress(self, file_bytes):
        ...


class SnappyCompression(CompressionBase):
    def __init__(self, *args, **kwargs):
        ...

    @functools.lru_cache
    def compress(self, file_bytes):
        return snappy.compress(str(self.file_bytes))

    @functools.lru_cache
    def decompress(self, file_bytes):
        return snappy.uncompress(str(self.file_bytes))


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
        self.compression_level = self.config["enhancement-settings"]["compression"]

    def get_compression_method(self, n: int):
        if n == 1:
            return Lz4Compression()
        if n == 2:
            return ZlibCompression()
        if n == 3:
            return LzfCompression()
        if n == 4:
            return SnappyCompression()

    def apply_compression(self, file_bytes):
        return self.get_compression_method(int(self.compression_level)).compress(
            file_bytes=file_bytes
        )

    def apply_decompression(self, file_bytes):
        return self.get_compression_method(int(self.compression_level)).decompress(
            file_bytes=file_bytes
        )

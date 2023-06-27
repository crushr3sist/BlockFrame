import hashlib
import math
import os
import pathlib
import tempfile
import uuid
from datetime import datetime, timedelta

from ..database_service.defaultmodel import ChunkHashes, DefaultChunkModel


class ChunksExistsError(Exception):
    pass


# The ChunkHandler class initializes various attributes related to chunking files.
class ChunkHandler:
    def __init__(self, *args, **kwargs) -> None:
        self.config = kwargs.get("config")
        self.path = self.config["file-storage-path"]
        self.option = kwargs.get("option")
        self.chunking_method: str = ""
        self.db = kwargs.get("db")
        self.chunk_size_estimate = 1024 * 1024
        self.chunk_counter = 0
        self.window_size = 10
        self.chunk_time_estimate = timedelta(seconds=1)
        self.compressor = kwargs.get("enhancements")

    def target(
        self,
        file_bytes=None,
        file_name=None,
        size=None,
        files: list = None,
        custom_chunker: callable = None,
    ):
        """
        This function sets various attributes related to a file, including its name, size, and hash values.

        :param file_bytes: A bytes object representing the contents of a file
        :param file_name: The name of the file to be targeted for chunking and hashing
        :param size: The size parameter is used to specify the size of the file in bytes. It is an optional
        parameter and can be used to provide the size of the file if it is not provided in the file_bytes
        parameter
        :param files: A list of file paths to be included in the target
        :type files: list
        :param custom_chunker: A callable function that can be used to customize the chunking process of the
        file
        :type custom_chunker: callable
        """
        self.custom_chunker = custom_chunker
        self.primary_uuid = uuid.uuid4()
        self.original_file_hash = ""
        self.chunk_file_hashes = []
        self.file_name = file_name
        self.file_bytes = file_bytes
        self.chunk_file_uid = []
        self.files = files
        self.size = size
        self.compressed_flag = False
        if file_bytes:
            with tempfile.NamedTemporaryFile(delete=True) as temp_file:
                if file_name and isinstance(file_name, str):
                    self.file_name = file_name
                else:
                    temp_file.write(file_bytes)
                    self.file_name = temp_file.name

        if self.file_bytes and self.file_name is not None:
            raise ValueError("Please either provide file_name or file_bytes")

        if self.file_name is None:
            raise ValueError("Either file_bytes or file_name must be provided")

        if self.config["enhancements"]["compress"]:
            self.compress_file()
            self.compressed_flag = True

        elif not pathlib.Path(self.file_name).exists:
            raise FileNotFoundError(f"{self.file_name} does not exist")

    def compress_file(self):
        if self.file_name:
            file_bytes = open(self.file_name, "rb").read()
            self.file_bytes = self.compressor.compression.apply_compression(file_bytes)
            self.compressed_flag = True

    def generic_chunks(self):
        """
        This function generates chunks of a file's bytes based on a specified size.
        """
        if self.file_bytes:
            _size = len(self.file_bytes) // self.size
            for i in range(self.size):
                yield self.file_bytes[i * _size : (i + 1) * _size]
        else:
            _size = os.stat(self.file_name).st_size // self.size
            with open(self.file_name, "rb") as f:
                while content := f.read(_size):
                    yield content

    def time_based_chunks(self):
        """
        This function reads a file in chunks and estimates the time required to transfer the remaining data
        based on the transfer rate of the previous chunks.
        """
        self.chunk_counter = 0
        with open(self.file_name, "rb") as f:
            if self.compressed_flag == True:
                f = self.file_bytes
            while True:
                start_time = (
                    datetime.now()
                )  # time the transfer of the previous chunk started
                content = f.read(self.chunk_size_estimate)
                if not content:
                    break
                yield content
                self.chunk_counter += 1
                end_time = (
                    datetime.now()
                )  # time the transfer of the current chunk ended
                transfer_time = end_time - start_time
                if self.chunk_counter % self.window_size == 0:
                    # use a sliding window to estimate the rate of data transfer
                    past_transfers = [transfer_time] * self.window_size
                    transfer_rate = sum(past_transfers, timedelta(0)) / self.window_size
                    # predict the time required to transfer the remaining data
                    remaining_bytes = os.stat(self.file_name).st_size - f.tell()
                    remaining_time_estimate = (
                        remaining_bytes / transfer_rate.total_seconds()
                    )
                    self.chunk_time_estimate = (
                        remaining_time_estimate / self.window_size
                    )
                    self.chunk_size_estimate = int(
                        max(
                            min(
                                self.chunk_size_estimate,
                                remaining_bytes / (self.chunk_time_estimate + 1),
                            ),
                            1,
                        )
                    )

    def secure_chunks(self):
        """
        This function generates secure chunks of a file by adjusting the chunk size based on collision
        probability.
        """
        with open(self.file_name, "rb") as f:
            if self.compressed_flag == True:
                f = self.file_bytes
                file_size = os.stat(self.file_name).st_size
            while True:
                chunk_size = self.chunk_size_estimate
                num_chunks = math.ceil(file_size / chunk_size)
                if num_chunks >= 4:
                    break
                chunk_size = math.ceil(file_size / 4)
                self.chunk_size_estimate = chunk_size

            while content := f.read(chunk_size):
                yield content
                self.chunk_counter += 1
                if self.chunk_counter % self.window_size == 0:
                    # use a sliding window to estimate the collision probability
                    past_hashes = self.hasher.digest() * self.window_size
                    self.hasher = hashlib.sha256()
                    self.hasher.update(past_hashes)
                    collision_probability = 1 - (1 - 1 / 2**256) ** self.window_size
                    # adjust the chunk size based on the collision probability
                    self.chunk_size_estimate = int(
                        max(
                            min(
                                self.chunk_size_estimate,
                                math.sqrt(
                                    0.5
                                    / collision_probability
                                    * os.stat(self.file_name).st_size
                                ),
                            ),
                            1,
                        )
                    )

    def produce_chunks(self):
        """
        This function produces chunks of a file based on different options and saves them to a directory
        while also calculating their hashes.
        """
        if self.option == "custom":
            split_files = self.custom_chunker(self.file_name, self.size)

        else:
            match self.option:
                case "generic":
                    split_files = self.generic_chunks()
                case "hardware":
                    split_files = self.hardware_chunks()
                case "time":
                    split_files = self.time_based_chunks()
                case "secure":
                    split_files = self.secure_chunks()
        [
            x
            for x in os.listdir(self.path)
            if x.startswith(f"{self.primary_uuid}_chunk_")
        ]

        with self.db as session:
            if (
                session.query(DefaultChunkModel)
                .filter_by(file_name=self.file_name)
                .all()
            ):
                raise ChunksExistsError("file is already chunked")

        count = 0
        for chunk in split_files:
            _hash = hashlib.sha256()
            _file_chunk_uid = uuid.uuid4()
            chunk_name = f"{self.primary_uuid}_chunk_{_file_chunk_uid}_{count}.chunk"
            if not pathlib.Path(self.path).is_dir():
                pathlib.Path(self.path).mkdir()

            with open(
                f"{pathlib.Path(self.path).absolute()}/{chunk_name}",
                "wb+",
            ) as f:
                _hash.update(f.read())
                count += 1
                f.write(bytes(chunk))
            self.chunk_file_uid.append(_file_chunk_uid)
            self.chunk_file_hashes.append(_hash.hexdigest())

    def hasher(self):
        """
        This function calculates the SHA256 hash of a file in chunks of 1024 bytes.
        """
        _hash = hashlib.sha256()
        with open(self.file_name, "rb") as file:
            chunk = 0
            while chunk != b"":
                chunk = file.read(1024)
                _hash.update(chunk)
        self.original_file_hash = _hash.hexdigest()

    def find_chunks_from_name(self):
        """
        This function returns the number of files in a directory that start with a specific string.
        :return: The function `find_chunks_from_name` returns the number of files in the directory specified
        by `self.path` that start with the string `"{self.primary_uuid}_chunk_"`.
        """
        return len(
            [
                x
                for x in os.listdir(self.path)
                if x.startswith(f"{self.primary_uuid}_chunk_")
            ]
        )

    def save_to_db(self):
        """
        This function saves information about a file and its chunks to a database.
        """
        with self.db as session:
            model = DefaultChunkModel(
                file_uuid=str(self.primary_uuid),
                file_name=self.file_name,
                size=self.find_chunks_from_name(),
                original_file_hash=self.original_file_hash,
                split_length=len(self.chunk_file_uid),
                linking_id=str(self.primary_uuid),
                compression_int=self.config["enhancement-settings"]["compression"],
            )
            for _hash, _uid in zip(self.chunk_file_hashes, self.chunk_file_uid):
                model.hashes.append(
                    ChunkHashes(
                        chunk_hash=_hash,
                        linking_id=str(self.primary_uuid),
                        chunk_length=len(_hash),
                        chunk_size=len(str(_uid)),
                    )
                )
            session.add(model)
            session.commit()

    def apply(self):
        """
        This function performs generic chunking, hashing, and saving to a database.
        """
        self.produce_chunks()
        self.hasher()
        self.save_to_db()

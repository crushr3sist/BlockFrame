import hashlib
import math
import os
import pathlib
import uuid
from datetime import datetime, timedelta

from ..database_service.defaultmodel import ChunkHashes, DefaultChunkModel


class ChunksExistsError(Exception):
    pass


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

    def target(
        self, file_name, size=None, files: list = None, custom_chunker: callable = None
    ):
        self.file_name = file_name
        self.size = size
        self.primary_uuid = uuid.uuid4()
        self.original_file_hash = ""
        self.chunk_file_hashes = []
        self.chunk_file_uid = []
        self.files = files
        self.custom_chunker = custom_chunker
        if not pathlib.Path(self.file_name) or not pathlib.Path(self.file_name).exists:
            raise FileNotFoundError
        return "correctly targeted"

    def generic_chunks(self):
        _size = os.stat(self.file_name).st_size // self.size
        with open(self.file_name, "rb") as f:
            while content := f.read(_size):
                yield content

    def time_based_chunks(self):
        self.chunk_counter = 0
        with open(self.file_name, "rb") as f:
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
                    # adjust the chunk size based on the predicted time to optimize transfer time
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
        with open(self.file_name, "rb") as f:
            file_size = os.stat(self.file_name).st_size
            while True:
                chunk_size = self.chunk_size_estimate
                num_chunks = math.ceil(file_size / chunk_size)
                if num_chunks >= 4:
                    break
                chunk_size = math.ceil(file_size / 4)
                num_chunks = 4
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
        existing_chunks = [
            x
            for x in os.listdir(self.path)
            if x.startswith(f"{self.primary_uuid}_chunk_")
        ]

        with self.db as session:
            if existing_models := (
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
        _hash = hashlib.sha256()
        with open(self.file_name, "rb") as file:
            chunk = 0
            while chunk != b"":
                chunk = file.read(1024)
                _hash.update(chunk)
        self.original_file_hash = _hash.hexdigest()

    def find_chunks_from_name(self):
        return len(
            [
                x
                for x in os.listdir(self.path)
                if x.startswith(f"{self.primary_uuid}_chunk_")
            ]
        )

    def save_to_db(self):
        with self.db as session:
            model = DefaultChunkModel(
                file_uuid=str(self.primary_uuid),
                file_name=self.file_name,
                size=self.find_chunks_from_name(),
                original_file_hash=self.original_file_hash,
                split_length=len(self.chunk_file_uid),
                linking_id=str(self.primary_uuid),
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

    def generic_chunking(self):
        self.produce_chunks()
        self.hasher()
        self.save_to_db()
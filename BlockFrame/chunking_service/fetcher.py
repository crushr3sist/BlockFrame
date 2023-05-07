from typing import Iterable
from ..database_service.defaultmodel import DefaultChunkModel
import glob
import re


class Fetcher:
    def __init__(self, *args, **kwargs) -> None:
        self.config = kwargs.get("config")
        self.path = self.config["file-storage-path"]
        self.db = kwargs.get("db")

    def target(self, file: Iterable[str] | str):
        self.file = file

        with self.db as session:
            self.file_id = (
                session.query(DefaultChunkModel)
                .filter_by(file_name=self.file.split("_")[0])
                .first()
            )

    def collect_chunks(self) -> list[str]:
        if isinstance(Iterable, type(self.file)):
            matching_files = []
            for f in self.file:
                matching_files.extend(glob.glob(f"{self.path}/{f}*"))
            matching_files.sort(key=lambda x: int(re.findall(r"\d+", x)[-2]))
            return matching_files

        return sorted(
            glob.glob(f"{self.path}/*{self.file_id.file_uuid}*"),
            key=lambda file: int(file.split("_")[-1].split(".")[0]),
        )

    def construct_file(self):
        self.file_bytes = b""
        for chunk in self.collect_chunks():
            with open(chunk, "rb") as chunk_file:
                self.file_bytes += chunk_file.read()

    def fetch(self):
        self.construct_file()
        with open(f"./reconstructed/{self.file_id.file_name}", "wb+") as f:
            f.write(self.file_bytes)

    def as_bytes(self):
        return self.file_bytes

    def as_fileobjs(self):
        return self.file_being_constructed

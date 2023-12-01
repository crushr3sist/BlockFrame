import glob
import re
import time
from typing import Iterable

from ..database_service.defaultmodel import DefaultChunkModel


class Fetcher:
    def __init__(self, *args, **kwargs) -> None:
        self.config = kwargs.get("config")
        self.path = self.config["file-storage-path"]
        self.db = kwargs.get("db")
        self.decompression = kwargs.get("enhancements")
        self.enhancements = kwargs.get("enhancements")

    def target(self, file: Iterable[str] | str):
        """
        This function retrieves the file ID from a database based on the file name.

        :param file: The `file` parameter is either a string or an iterable of strings. It is used as input
        to the `target` method of a class. The method assigns the value of `file` to the `self.file`
        attribute of the class instance. The method then queries a database using the `
        :type file: Iterable[str] | str
        """

        self.file = file

        with self.db as session:
            self.file_id = (
                session.query(DefaultChunkModel)
                .filter_by(file_name=self.file.split("_")[0])
                .first()
            )

    def collect_chunks(self) -> list[str]:
        """
        This function collects and returns a list of file paths that match a certain pattern.
        :return: The function `collect_chunks` returns a list of file paths that match a certain
        pattern. The pattern depends on the type of `self.file`. If `self.file` is an iterable, the
        function searches for files in the directory `self.path` that match the pattern
        `{self.path}/{f}*`, where `f` is an element of `self.file`. If `self.file` is not
        """
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
        """
        This function constructs a file by reading binary data from multiple chunks and concatenating them
        into a single byte string.
        """
        self.file_bytes = b""
        for chunk in self.collect_chunks():
            with open(chunk, "rb") as chunk_file:
                chunk_data = chunk_file.read()
                print(f"Appending {len(chunk_data)} bytes from {chunk}")
                self.file_bytes += chunk_data

    def fetch(self):
        """
        This function fetches a file by constructing it and writing its bytes to a new file.
        """
        self.construct_file()
        time.sleep(0.05)
        output_path = f"./reconstructed/{self.file_id.file_name}"
        print(f"secret key: {self.file_id.secret_key}")

        with open(output_path, "wb+") as f:
            decrypted_bytes = self.file_bytes

            if self.config["enhancements"]["encrypt"]:
                # Assuming your file query object has an attribute 'secret_key'
                decryption_key = self.file_id.secret_key
                print(f"Decrypting {len(decrypted_bytes)} bytes...")
                decrypted_bytes = self.enhancements.encryption.apply_decryption(
                    decrypted_bytes, decryption_key
                )
                print(
                    f"Decryption complete. Decrypted size: {len(decrypted_bytes)} bytes"
                )

            if self.config["enhancements"]["compress"]:
                print(f"Decompressing {len(decrypted_bytes)} bytes...")
                decompressed_bytes = self.decompression.compression.apply_decompression(
                    decrypted_bytes
                )
                print(
                    f"Decompression complete. Decompressed size: {len(decompressed_bytes)} bytes"
                )
                f.write(decompressed_bytes)
            else:
                f.write(decrypted_bytes)

        print(f"File fetched and saved to: {output_path}")

    def as_bytes(self):
        return self.file_bytes

    def as_fileobjs(self):
        return self.file_being_constructed

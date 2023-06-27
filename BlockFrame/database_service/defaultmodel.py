from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Relationship

from BlockFrame.database_service.initalisation import DatabaseInterface


class DefaultChunkModel(DatabaseInterface().Base):
    __tablename__ = "ChunkModel-default"
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_uuid = Column(String)
    file_name = Column(String)
    size = Column(Integer)
    original_file_hash = Column(String)
    split_length = Column(Integer)
    linking_id = Column(String)
    compression_int = Column(Integer)
    hashes = Relationship("ChunkHashes", backref="default_chunk")

    def __init__(self, *args, **kwargs):
        self.file_uuid = kwargs.get("file_uuid")
        self.file_name = kwargs.get("file_name")
        self.size = kwargs.get("size")
        self.original_file_hash = kwargs.get("original_file_hash")
        self.split_length = kwargs.get("split_length")
        self.linking_id = kwargs.get("linking_id")
        self.hashes = kwargs.get("hashes", [])
        self.compression_int = kwargs.get("compression_int")


class ChunkHashes(DatabaseInterface().Base):
    __tablename__ = "ChunkModel-hashes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chunk_hash = Column(String)
    linking_id = Column(String, ForeignKey("ChunkModel-default.id"))
    chunk_length = Column(Integer)
    chunk_size = Column(Integer)

    def __init__(self, *args, **kwargs):
        self.chunk_hash = kwargs.get("chunk_hash")
        self.linking_id = kwargs.get("linking_id")
        self.chunk_length = kwargs.get("chunk_length")
        self.chunk_size = kwargs.get("chunk_size")

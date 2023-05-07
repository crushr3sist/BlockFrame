import pytest
import pathlib
import shutil
import BlockFrame
from BlockFrame.chunking_service.chunking import ChunksExistsError
from BlockFrame.database_service.defaultmodel import DefaultChunkModel


@pytest.fixture(scope="session")
def config_path():
    return pathlib.Path("./config.json").absolute()


@pytest.fixture(scope="session")
def bf(config_path):
    bf = block_frame.BlockFrame(config_path, option="generic")
    yield bf
    shutil.rmtree(str(bf.fetcher.working_dir))


@pytest.fixture()
def empty_db(bf):
    bf.database.delete_table(DefaultChunkModel)
    bf.database.create_table(DefaultChunkModel)


def test_target_with_valid_file(bf):
    assert bf.chunker.target("tests/image.jpg", size=5) == "correctly targetted"


def test_target_with_missing_file(bf):
    with pytest.raises(FileNotFoundError):
        bf.chunker.target("tests/non_existent_file.jpg", size=5)


def test_target_with_invalid_chunk_size(bf):
    with pytest.raises(ValueError):
        bf.chunker.target("tests/image.jpg", size=0)
    with pytest.raises(ValueError):
        bf.chunker.target("tests/image.jpg", size=-1)


def test_chunk_twice(bf):
    bf.chunker.target("tests/image.jpg", size=5)
    bf.chunker.generic_chunking()
    with pytest.raises(ChunksExistsError) as cm:
        bf.chunker.target("tests/image.jpg", size=5)
        bf.chunker.generic_chunking()
    assert str(cm.value) == "file is already chunked"


def test_chunk_and_fetch(bf, empty_db):
    bf.chunker.target("tests/image.jpg", size=5)
    bf.chunker.generic_chunking()
    assert len(bf.database.get_all()) == 1
    bf.fetcher.target("tests/image.jpg")
    chunks = bf.fetcher.collect_chunks()
    assert len(chunks) == 5
    bf.fetcher.fetch()
    with open("tests/image.jpg", "rb") as f1, open("tests/image_copy.jpg", "rb") as f2:
        assert f1.read() == f2.read()

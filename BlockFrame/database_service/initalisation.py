from sqlalchemy.engine import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from abc import ABC


class DatabaseInterface(ABC):
    Base = declarative_base()
    db_engine = create_engine("sqlite:///block_frame.db")
    sync_session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

    @classmethod
    def custom_uri(cls, uri: str):
        cls.db_engine = create_engine(uri)
        cls.sync_session = sessionmaker(
            autocommit=False, autoflush=False, bind=cls.db_engine
        )

    @classmethod
    def return_engine(cls):
        return cls.db_engine


class BlockFrameDatabaseInit(DatabaseInterface):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.class_model = kwargs.get("class_model")
        if self.class_model is None:
            from defaultmodel import DefaultChunkModel

            self.db_model = DefaultChunkModel
        else:
            self.db_model = self.class_model

    def create_table(self, db_model):
        with self.db_engine.begin() as conn:
            self.sync_session(bind=conn)  # <-- change this line
            db_model.metadata.create_all(conn)

    def get_db(self):
        # return an object which can be used to commit data to the database easily
        return self.sync_session()


class BlockFrameModelInstance(DatabaseInterface):
    def __new__(cls):
        instance = super().__new__(cls)
        return instance.Base

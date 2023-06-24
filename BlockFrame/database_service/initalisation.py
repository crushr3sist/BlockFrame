from abc import ABC

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


class DatabaseInterface(ABC):
    Base = declarative_base()
    db_engine = create_engine("sqlite:///block_frame.db")
    sync_session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

    @classmethod
    def custom_uri(cls, uri: str):
        """
        This is a class method that creates a database engine and session using the provided URI.

        :param cls: "cls" is a reference to the class itself, which means that this method is a class
        method. It can be called on the class itself rather than on an instance of the class
        :param uri: The URI (Uniform Resource Identifier) is a string that specifies the location of a
        database. It typically includes information such as the database type, host name, port number, and
        database name
        :type uri: str
        """
        cls.db_engine = create_engine(uri)
        cls.sync_session = sessionmaker(
            autocommit=False, autoflush=False, bind=cls.db_engine
        )

    @classmethod
    def return_engine(cls):
        """
        This is a class method that returns the database engine of the class.

        :param cls: "cls" is a commonly used abbreviation for "class" in Python. In this context, it refers
        to the class itself, rather than an instance of the class. The "@classmethod" decorator indicates
        that this method is a class method, which means it can be called on the class itself rather than
        :return: The method `return_engine` is returning the `db_engine` attribute of the class.
        """
        return cls.db_engine


class BlockFrameDatabaseInit(DatabaseInterface):
    def __init__(self, *args, **kwargs) -> None:
        """
        This function initializes an object with a default or user-specified model.
        """
        super().__init__()
        self.class_model = kwargs.get("class_model")
        if self.class_model is None:
            from defaultmodel import DefaultChunkModel

            self.db_model = DefaultChunkModel
        else:
            self.db_model = self.class_model

    def create_table(self, db_model):
        """
        This function creates a database table using the metadata of a given database model.

        :param db_model: The db_model parameter is likely an instance of a SQLAlchemy model class that
        represents a database table. It contains information about the table's columns, data types, and
        relationships with other tables. The create_table method uses this information to generate the
        SQL code necessary to create the table in the database
        """
        with self.db_engine.begin() as conn:
            self.sync_session(bind=conn)
            db_model.metadata.create_all(conn)

    def get_db(self):
        return self.sync_session()


class BlockFrameModelInstance(DatabaseInterface):
    def __new__(cls):
        """
        This is a constructor method that creates a new instance of a class and returns the instance's base
        attribute.

        :param cls: The cls parameter refers to the class that the method is being called on. In this case,
        it is the class that the __new__ method is defined in
        :return: The code will raise an AttributeError because `instance.Base` is not a valid attribute. It
        seems like the intention was to return `instance` instead.
        """
        instance = super().__new__(cls)
        return instance.Base

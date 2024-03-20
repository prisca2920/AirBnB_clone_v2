#!/usr/bin/python3
"""Creating a new engine `DBStorage`"""
import os
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from models.city import City
from models.state import State
from models.place import Place
from models.amenity import Amenity
from models.user import User
from models.review import Review


class DBStorage:
    """Represents a database storage engine.

    Methods:
        __init__: Initializes a new instance of DBStorage.
        all: Queries the database.
        new: Adds the object to the current database session.
        save: Commits all changes.
        delete: Deletes from the current database session.
        reload: Creates all tables in the database and creates the current
            database session.
    """

    __engine = None
    __session = None

    def __init__(self):
        """Initializes a new instance"""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}"
                                       .format(os.environ.get("HBNB_MYSQL_USER"),
                                               os.environ.get("HBNB_MYSQL_PWD"),
                                               os.environ.get("HBNB_MYSQL_HOST"),
                                               os.environ.get("HBNB_MYSQL_DB")),
                                       pool_pre_ping=True)
        if os.environ.get("HBNB_ENV") == "test": 
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Queries the database.

        Args:
            cls (str): The class name to query. Defaults to None.

        Returns:
            dict: A dictionary containing queried objects.
        """
        if cls:
            res = self.__session.query(eval(cls)).all()
        else:
            res = self.__session.query(State).all()
            res.extend(self.__session.query(City).all())
            res.extend(self.__session.query(User).all())
            res.extend(self.__session.query(Place).all())
            res.extend(self.__session.query(Review).all())

        return {f"{type(obj).__name__}.{obj.id}": obj for obj in res}

        
    def new(self, obj):
        """add the object to the current database session.

        Args:
            obj (BaseModel): The object to add to the session
        """
        self.__session.add(obj)

    def save(self):
        """commits all changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes from the current database session.

        Args:
            obj (BaseModel): The object to delete from the session.
                Defaults to None.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database
        and creates the current database session
        """
        Base.metadata.create_all(self.__engine)
        db_session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(db_session)()

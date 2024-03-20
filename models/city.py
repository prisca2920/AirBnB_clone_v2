#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

class City(BaseModel, Base):
    """The city class, contains state ID and name

    Attributes:
        state_id (str): The ID of the state where the city is located.
        name (str): The name of the city.
        places (relationship): Relationship to Place model, representing
            places in the city.
    """
    __tablename__ = "cities"
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
    name = Column(String(128), nullable=False)
    places = relationship("Place", backref="cities", cascade="all, delete")

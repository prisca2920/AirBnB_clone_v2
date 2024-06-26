#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import relationship
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.user import User
from models.review import Review


class Place(BaseModel, Base):
    """A place to stay

    Attributes:
        city_id (str): The ID of the city where the place is located.
        user_id (str): The ID of the user who owns the place.
        name (str): The name of the place.
        description (str): The description of the place.
        number_rooms (int): The number of rooms in the place.
        number_bathrooms (int): The number of bathrooms in the place.
        max_guest (int): The maximum number of guests
            allowed in the place.
        price_by_night (int): The price per night
            for staying in the place.
        latitude (float): The latitude coordinate of the place.
        longitude (float): The longitude coordinate of the place.
        amenity_ids (list): List of amenity
            IDs associated with the place.
        reviews (relationship): Relationship to Review model,
            representing reviews for the place.
        place_amenity(Table): Define association table
            for many-to-many relationship
        amenities(relationship): Establish many-to-many relationship
            with Amenity

        Methods:
            -amenities(self): Defines getter for amenities attribute
            -amenities(self, amenity): Defines setter for amenities
                attribute
    """

    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id',
                                 String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True,
                                 nullable=False),
                          Column('amenity_id',
                                 String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True,
                                 nullable=False)
                          )
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    reviews = relationship("Review",
                           cascade="all, delete",
                           backref="place"
                           )
    amenities = relationship("Amenity",
                             secondary=place_amenity,
                             viewonly=False
                             )

    @property
    def amenities(self):
        """Getter for amenities attribute"""
        return [amenity.id for amenity in self.amenities]

    @amenities.setter
    def amenities(self, amenity):
        """Setter for amenities attribute"""
        if isinstance(amenity, Amenity):
            self.amenities.append(amenity.id)

from enum import Enum
from pydantic import BaseModel, ConfigDict, field_validator
from typing import List

class Geolocation(BaseModel):
    """
    Defines a particular geolocation point or area related to the associated record or product.  It is made up of a
    List of Point values (latitude, longitude pairs) making up the geolocation construct.
    """
    model_config = ConfigDict(validate_assignment=True)

    class Type(Enum):
        """
        Indicates the TYPE of this particular geolocation construct.
        A POINT is a single set of latitude and longitude.
        A BOX indicates a NW and SE pair of latitude and longitude points making up the box area.
        A POLYGON should be any number of latitude and longitude pairs, starting and ending with the same value to complete
        the polygon construct.
        """
        POINT="Point"
        BOX="BOX"
        POLYGON="POLYGON"

    class Point(BaseModel):
        """
        Represents a single POINT, or pair of latitude and longitude values, that makes up part of the geolocation.
        """
        model_config = ConfigDict(validate_assignment=True)

        latitude: float
        longitude: float

        @field_validator("latitude")
        @classmethod
        def validate_latitude(cls, lat) -> float:
            if not isinstance(lat, (int, float)):
                raise ValueError("Latitude value is not numeric.")
            
            if abs(lat)>90:
                raise ValueError('Latitude must be between -90 and 90.')
            return lat
        
        @field_validator("longitude")
        @classmethod
        def validate_longitude(cls, value) -> float:
            if not isinstance(value, (int, float)):
                raise ValueError('Longitude is not numeric.')
            
            if abs(value) > 180:
                raise ValueError('Longitude must be between -180 and 180.')
            return value
     
    type: str = None
    label: str = None
    points: List[Point]

    def add(self, point: Point):
        if not isinstance(point, self.Point):
            raise ValueError('Indicated point is not a Geolocation.Point.')
        if self.points is None:
            self.points = []
        self.points.append(point)

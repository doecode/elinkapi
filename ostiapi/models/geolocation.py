from enum import Enum
from pydantic import BaseModel, ConfigDict, field_validator
from typing import List

class Geolocation(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    class Type(Enum):
        POINT="Point"
        BOX="BOX"
        POLYGON="POLYGON"

    class Point(BaseModel):
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

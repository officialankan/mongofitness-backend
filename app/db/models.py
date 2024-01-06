from enum import Enum
from typing import List
from bson import ObjectId
from pydantic import BaseModel
from datetime import datetime

class OID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if v == "":
            raise TypeError("ObjectId cannot be empty")
        if ObjectId.is_valid(v) is False:
            raise TypeError("Invalid ObjectId") 
        return str(v)
    
class BaseDBMoodel(BaseModel):
    model_config = {
        "from_attributes": True,
        "populate_by_name": True
                    }
        
class DailySteps(BaseDBMoodel):
    ts: datetime
    steps: int

class SportType(str, Enum):
    AlpineSki = "AlpineSki"
    BackCountrySki = "BackCountrySki"
    Badminon = "Badminon"
    Canoeing = "Canoeing"
    Crossfit = "Crossfit"
    EBikeRide = "EBikeRide"
    Elliptical = "Elliptical"
    EMountainBikeRide = "EMountainBikeRide"
    Golf = "Golf"
    GravelRide = "GravelRide"
    Handcycle = "Handcycle"
    HighIntensityIntervalTraining = "HighIntensityIntervalTraining"
    Hike = "Hike"
    IceSkate = "IceSkate"
    InlineSkate = "InlineSkate"
    Kayaking = "Kayaking"
    KiteSurf = "KiteSurf"
    MountainBikeRide = "MountainBikeRide"
    NordicSki = "NordicSki"
    Pickleball = "Pickleball"
    Pilates = "Pilates"
    Racquetball = "Racquetball"
    Ride = "Ride"
    RockClimbing = "RockClimbing"
    RollerSki = "RollerSki"
    Rowing = "Rowing"
    Run = "Run"
    Sail = "Sail"
    Skateboard = "Skateboard"
    Snowboard = "Snowboard"
    Snowshoe = "Snowshoe"
    Soccer = "Soccer"
    Squash = "Squash"
    StairStepper = "StairStepper"
    StandUpPaddling = "StandUpPaddling"
    Surfing = "Surfing"
    Swim = "Swim"
    TableTennis = "TableTennis"
    Tennis = "Tennis"
    TrailRun = "TrailRun"
    Velomobile = "Velomobile"
    VirtualRide = "VirtualRide"
    VirtualRow = "VirtualRow"
    VirtualRun = "VirtualRun"
    Walk = "Walk"
    WeightTraining = "WeightTraining"
    Wheelchair = "Wheelchair"
    Windsurf = "Windsurf"
    Workout = "Workout"
    Yoga = "Yoga"

class ActivityTypeByDate(BaseDBMoodel):
    ts: datetime
    sport_type: List[SportType]

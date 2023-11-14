from typing import Optional
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
    
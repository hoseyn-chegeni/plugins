from pydantic import BaseModel
from typing import Optional

class CollegeData(BaseModel):
	href:str
	value:str

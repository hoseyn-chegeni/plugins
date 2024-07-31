from pydantic import BaseModel
from typing import Optional

class CollegeData(BaseModel):
    href: Optional[str] = None
    value: Optional[str] = None

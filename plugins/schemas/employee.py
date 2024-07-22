from pydantic import BaseModel
from typing import List, Optional


class Employee(BaseModel):
    department: Optional[str] = None
    image: Optional[str] = None
    name: Optional[str] = None
    role: Optional[str] = None
    internal_number: Optional[str] = None
    phone_number: Optional[str] = None
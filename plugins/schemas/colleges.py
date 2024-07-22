from pydantic import BaseModel


class CollegeData(BaseModel):
    href: str
    value: str

from pydantic import BaseModel
from datetime import datetime


class News(BaseModel):
    date: datetime = datetime(1990, 1, 1)
    image: str = ""
    labels: list = []
    link: str = ""
    news_id: str = ""
    text: str = ""
    title: str = ""

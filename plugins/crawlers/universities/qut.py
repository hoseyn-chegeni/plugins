import requests
from bs4 import BeautifulSoup
from schemas import colleges
from crawlers.universities.base import University
from crawlers.utils import check_connection
from schemas import Course, Professor, Skill, Book, Honor
from schemas.employee import Employee
import xml.etree.ElementTree as ET
from typing import Generator
import re


class ElmSanatCrawler(University):
    def __init__(self) -> None:
        self.url = ""

    def get_employees(self):
        pass

    def get_colleges(self):
        pass

    def get_professors(self):
        pass

    def get_professor_page(self, link: str):
        pass

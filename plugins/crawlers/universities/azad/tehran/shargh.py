from bs4 import BeautifulSoup
from crawlers.universities.base import University
from schemas.employee import Employee
from playwright.sync_api import sync_playwright
from schemas.colleges import CollegeData
from schemas.professor import (
    Professor,
    EducationalRecord,
    JobExperience,
    Activity,
    Honor,
)
import re


class TehranSharghCrawler(University):
    def __init__(self) -> None:
        self.url = ""

    def get_employees(self):
        pass

    def get_colleges(self):
        pass
    def get_professors(self):
        pass
    def get_professor_page(self, link) -> Professor:
        pass
    def get_employee_page(self) -> Employee:
        return super().get_employee_page()

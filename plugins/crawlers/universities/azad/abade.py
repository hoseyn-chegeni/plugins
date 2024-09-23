from bs4 import BeautifulSoup
from crawlers.universities.base import University
from schemas.employee import Employee
from playwright.sync_api import sync_playwright
from schemas.colleges import CollegeData
from schemas.professor import (
    Professor,
)
import re


class Crawler(University):
    def __init__(self) -> None:
        self.url = ""

    def get_employees(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://abadeh.iau.ir/fa/page/163/%D8%B4%D9%85%D8%A7%D8%B1%D9%87-%D8%AA%D9%85%D8%A7%D8%B3-%D9%87%D8%A7%DB%8C-%D9%88%D8%A7%D8%AD%D8%AF")
            page.wait_for_selector('tbody')
            page_content = page.content()
            browser.close()

        soup = BeautifulSoup(page_content, 'html.parser')
        rows = soup.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            
            if len(columns) == 3:
                name = columns[0].text.strip()
                id_number = columns[1].text.strip()
                phone_number = columns[2].text.strip()
                employee = Employee(name=name, internal_number=id_number, phone_number=phone_number)
                yield employee
    


    def get_colleges(self):
        pass

    def get_professors(self):
        pass

    def get_professor_page(self, link) -> Professor:
        pass

    def get_employee_page(self) -> Employee:
        return super().get_employee_page()

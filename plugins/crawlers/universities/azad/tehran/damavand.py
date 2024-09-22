from bs4 import BeautifulSoup
from crawlers.universities.base import University
from schemas.employee import Employee
from playwright.sync_api import sync_playwright
from schemas.colleges import CollegeData
from schemas.professor import (
    Professor,
)
import re


class DamavandCrawler(University):
    def __init__(self) -> None:
        self.url = "https://damavand.iau.ir/"

    def get_employees(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://damavand.iau.ir/fa/grid/23/%D8%AF%D9%81%D8%AA%D8%B1%DA%86%D9%87-%D8%AA%D9%84%D9%81%D9%86?GridSearch%5BpageSize%5D=200&GridSearch%5Bsearch%5D=")
            page.wait_for_selector('tbody')
            page_content = page.content()
            browser.close()


        soup = BeautifulSoup(page_content, "html.parser")
        tbody = soup.find('tbody')
        rows = tbody.find_all('tr')
        
        for row in rows:
            columns = row.find_all('td')
            if columns[1].get_text(strip=True) != '-':
                name = columns[1].get_text(strip=True)
                role = columns[2].get_text(strip=True)
                internal = columns[3].get_text(strip=True)
                phone = columns[4].get_text(strip=True)
                dept = columns[5].get_text(strip=True)

                emp = Employee(name = name, role=role, internal_number= internal, phone_number=phone, department=dept)
                yield emp




    def get_colleges(self):

        pass

    def get_professors(self):
        pass


    def get_professor_page(self, link) -> Professor:
        pass
    def get_employee_page(self) -> Employee:
        return super().get_employee_page()

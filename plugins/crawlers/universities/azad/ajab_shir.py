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
        pass

    def get_colleges(self):
        pass

    def get_professors(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(
                "https://ajabshir.iau.ir/fa/grid/3/%D8%A7%D8%B9%D8%B6%D8%A7%DB%8C-%D9%87%DB%8C%D8%A7%"
            )
            page.wait_for_selector("table.table-striped")
            page_content = page.content()
            browser.close()

        soup = BeautifulSoup(page_content, "html.parser")
        table = soup.find("table", class_="table-striped")
        rows = table.find("tbody").find_all("tr")
        for row in rows:

            columns = row.find_all("td")

            name = columns[1].get_text(strip=True)
            rank = columns[2].get_text(strip=True)
            major = columns[3].get_text(strip=True)

            professor = Professor(full_name=name, rank=rank, major=major)
            yield professor

    def get_professor_page(self, link) -> Professor:
        pass

    def get_employee_page(self) -> Employee:
        return super().get_employee_page()

from bs4 import BeautifulSoup
from crawlers.universities.base import University
from schemas.employee import Employee
from playwright.sync_api import sync_playwright
from schemas.colleges import CollegeData
from schemas.professor import (
    Professor,
)
import re


class ArakCrawler(University):
    def __init__(self) -> None:
        self.url = ""

    def get_employees(self):
        pass

    def get_colleges(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://arak.iau.ir/fa")
            page.wait_for_selector("ul#w3a8755a040adf602c2c7a92170abc59e8")
            page_content = page.content()
            browser.close()

        soup = BeautifulSoup(page_content, "html.parser")
        ul_elements = soup.find_all("ul", class_="dropdown-menu")
        for ul in ul_elements:
            links = ul.find_all("a", string=lambda text: text and "دانشکده" in text)
            for link in links:
                college = CollegeData(
                    href=link["href"], value=link.get_text(strip=True)
                )
                yield college

    def get_professors(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for page_number in range(1, 2):
                url = f"https://arak.iau.ir/humanities/fa/faculty"
                page.goto(url)
                page.wait_for_selector("form")
                content = page.content()

                soup = BeautifulSoup(content, "html.parser")
                tbody = soup.find("tbody")
                rows = tbody.find_all("tr")

                for row in rows:
                    columns = row.find_all("td")
                    if columns[1].get_text(strip=True) != "-":
                        last_name = columns[0].get_text(strip=True)
                        first_name = columns[1].get_text(strip=True)
                        faculty = columns[2].get_text(strip=True)
                        rank = columns[3].get_text(strip=True)
                        professor = Professor(
                            full_name=first_name + " " + last_name,
                            rank=rank,
                            faculty=faculty,
                        )
                        yield professor

            browser.close()

    def get_professor_page(self, link) -> Professor:
        pass

    def get_employee_page(self) -> Employee:
        return super().get_employee_page()

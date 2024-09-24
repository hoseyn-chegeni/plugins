from bs4 import BeautifulSoup
from crawlers.universities.base import University
from schemas.employee import Employee
from playwright.sync_api import sync_playwright
from schemas.colleges import CollegeData
from schemas.professor import (
    Professor,
)
import re


class AnarCrawler(University):
    def __init__(self) -> None:
        self.url = ""

    def get_employees(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(
                "https://anar.iau.ir/fa/grid/4/%D8%B1%D8%A7%D9%87%D9%86%D9%85%D8%A7%DB%8C-%D8%AC%D8%A7%D9%85%D8%B9-%D8%AA%D9%84%D9%81%D9%86-%D9%87%D8%A7%DB%8C-%D9%88%D8%A7%D8%AD%D8%AF?GridSearch%5BpageSize%5D=200&GridSearch%5Bsearch%5D="
            )
            page.wait_for_selector("tbody")
            page_content = page.content()
            browser.close()

        soup = BeautifulSoup(page_content, "html.parser")
        tbody = soup.find("tbody")
        rows = tbody.find_all("tr")

        for row in rows:
            columns = row.find_all("td")
            if columns[1].get_text(strip=True) != "-":
                name = columns[1].get_text(strip=True)
                lastname =  columns[2].get_text(strip=True)
                role = columns[3].get_text(strip=True)
                internal = columns[5].get_text(strip=True)
                phone = columns[6].get_text(strip=True)
                dept = columns[4].get_text(strip=True)

                emp = Employee(
                    name=name + ' ' + lastname,
                    role=role,
                    internal_number=internal,
                    phone_number=phone,
                    department=dept,
                )
                yield emp

    def get_colleges(self):
        pass

    def get_professors(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for page_number in range(1, 2):
                url = f"https://anar.iau.ir/fa/faculty?page={page_number}"
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

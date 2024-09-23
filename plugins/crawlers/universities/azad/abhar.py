from bs4 import BeautifulSoup
from crawlers.universities.base import University
from schemas.employee import Employee
from playwright.sync_api import sync_playwright
from schemas.colleges import CollegeData
from schemas.professor import (
    Professor,
)
import re


class AbharCrawler(University):
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
            page.goto("https://abhar.iau.ir/fa/faculty/faculty-list/1#22")
            page.wait_for_selector(".col-xs-8")
            page_content = page.content()
            browser.close()

        soup = BeautifulSoup(page_content, "html.parser")
        faculty_divs = soup.find_all("div", class_="col-xs-8")
        for faculty in faculty_divs:
            name_tag = faculty.find("h4", class_="heading")
            if name_tag:
                name = name_tag.get_text(strip=True)
            position_tag = faculty.find("i", class_="fa-graduation-cap")
            if position_tag:
                position_text = (
                    position_tag.next_sibling.strip()
                    if position_tag.next_sibling
                    else None
                )
                rank = position_text

            resume_link = faculty.find("a", href=re.compile(r"\.pdf$"))
            if resume_link:
                resume_url = resume_link["href"]
            professor = Professor(full_name=name, rank=rank)
            professor.socials.personal_cv = resume_url
            yield professor

    def get_professor_page(self, link) -> Professor:
        pass

    def get_employee_page(self) -> Employee:
        return super().get_employee_page()

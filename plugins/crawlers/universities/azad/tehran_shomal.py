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


class TehranShomalCrawler(University):
    def __init__(self) -> None:
        self.url = "https://ntb.iau.ir"

    def get_employees(self):
        pass

    def get_colleges(self):
        pass

    def get_professors(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for page_number in range(1, 19):
                url = f"https://ntb.iau.ir/faculty/fa?%2Ffa=&page={page_number}&per-page=18"
                page.goto(url)
                page.wait_for_selector("form")
                content = page.content()
                soup = BeautifulSoup(content, "html.parser")
                faculty_items = soup.find_all(
                    "div", class_="item grid-group-item col-sm-6 col-lg-4"
                )

                for item in faculty_items:
                    list_caption = item.find("div", class_="list-caption")
                    if list_caption:
                        link_tag = list_caption.find("a", href=True)
                        link = link_tag["href"]
                        yield link
            browser.close()

    def get_professor_page(self, link) -> Professor:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(link)
            page.wait_for_selector("thead")
            content = page.content()
            browser.close()

        soup = BeautifulSoup(content, "html.parser")
        main_info_div = soup.find("div", class_="block main-info")

        if main_info_div:
            name = main_info_div.find("div", class_="profile-usertitle-name").get_text(
                strip=True
            )
            rank = main_info_div.find("div", class_="profile-usertitle-job").get_text(
                strip=True
            )
            faculty_div = main_info_div.find(text=lambda x: "دانشکده" in x)
            faculty = faculty_div.split(":")[1].strip() if faculty_div else "Unknown"
            group_div = main_info_div.find(text=lambda x: "گروه" in x)
            group = group_div.split(":")[1].strip() if group_div else "Unknown"
            resume_link_tag = main_info_div.find("a", class_="btn btn-teal m-t-1")
            resume_link = resume_link_tag["href"] if resume_link_tag else None

            professor = Professor(
                full_name=name, rank=rank, group=group, faculty=faculty
            )
            professor.socials.personal_cv = self.url + resume_link
            return professor

        else:
            print("Main info block not found.")
            return None

    def get_employee_page(self) -> Employee:
        return super().get_employee_page()

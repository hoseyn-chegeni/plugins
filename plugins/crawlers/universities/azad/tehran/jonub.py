from bs4 import BeautifulSoup
from crawlers.universities.base import University
from schemas.employee import Employee
from playwright.sync_api import sync_playwright
from schemas.colleges import CollegeData
from schemas.professor import (
    Professor,
)
import re


class TehranJonubCrawler(University):
    def __init__(self) -> None:
        self.url = "https://stb.iau.ir/"

    def get_employees(self):
        pass

    def get_colleges(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://stb.iau.ir/fa")
            page.wait_for_selector("ul")
            page_content = page.content()
            browser.close()

        soup = BeautifulSoup(page_content, "html.parser")
        all_li_elements = soup.find_all("li")
        target_dropdown = None
        for li in all_li_elements:
            a_tag = li.find("a")
            if a_tag and re.search(r"دانشکده ها", a_tag.get_text()):
                target_dropdown = li
                break

        for li in target_dropdown.find_all("li"):
            a_tag = li.find("a")
            if a_tag:
                faculty_name = a_tag.get_text(strip=True)
                faculty_link = a_tag["href"]
                college = CollegeData(href=faculty_link, value=faculty_name)
                yield college

    def get_professors(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for page_number in range(1, 50):
                url = f"https://stb.iau.ir/faculty/fa?%2Ffa=&page={page_number}&per-page=18"
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
            page.wait_for_selector("ul")
            page_content = page.content()
            browser.close()

        soup = BeautifulSoup(page_content, "html.parser")
        main_info = soup.find("div", class_="block main-info")

        if main_info:

            img_tag = main_info.find("img", class_="img-responsive")
            img_url = "https://stb.iau.ir/" + img_tag["src"] if img_tag else None

            name_tag = main_info.find("div", class_="profile-usertitle-name")
            name = name_tag.get_text(strip=True) if name_tag else None

            job_title_tag = main_info.find("div", class_="profile-usertitle-job")
            job_title = job_title_tag.get_text(strip=True) if job_title_tag else None

            faculty_tag = main_info.find(text=lambda t: "دانشکده" in t)
            faculty = faculty_tag.split(":")[-1].strip() if faculty_tag else None

            group_tag = main_info.find(text=lambda t: "گروه" in t)
            group = group_tag.split(":")[-1].strip() if group_tag else None

            cv_link_tag = main_info.find("a", class_="btn btn-teal m-t-1")
            cv_link = (
                "https://stb.iau.ir/" + cv_link_tag["href"] if cv_link_tag else None
            )

            professor = Professor(
                full_name=name,
                rank=job_title,
                faculty=faculty,
                image=img_url,
                group=group,
            )
            professor.socials.personal_cv = cv_link
            return professor

    def get_employee_page(self) -> Employee:
        return super().get_employee_page()

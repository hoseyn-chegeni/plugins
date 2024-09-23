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
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://ahvaz.iau.ir/fa/page/51/%D8%AF%D8%A7%D9%86%D8%B4%DA%A9%D8%AF%D9%87-%D9%87%D8%A7")  
            page.wait_for_timeout(5000)  
            page_content = page.content()
            browser.close()

        soup = BeautifulSoup(page_content, "html.parser")
        li_elements = soup.find_all("li", class_="dropdown yamm-fw")
        target_text_pattern = re.compile(r'دانشکده‌ها')
        for li in li_elements:
            anchor_tag = li.find("a", class_="dropdown-toggle")

            if anchor_tag and target_text_pattern.search(anchor_tag.get_text(strip=True)):
                faculties = li.find_all("a")[1:]
                for faculty in faculties:
                    href = faculty.get("href")
                    text = faculty.get_text(strip=True)

                    college = CollegeData(href=href, value=text)
                    yield college

                    
    def get_professors(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for page_number in range(1, 50):
                url = f"https://ahvaz.iau.ir/faculty/fa?%2Ffa=&page={page_number}&per-page=18"
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
        pass

    def get_employee_page(self) -> Employee:
        return super().get_employee_page()

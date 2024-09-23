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
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://abadeh.iau.ir/fa")

            page.wait_for_selector('ul#w04007ba748339bbdae2f95cb5a80189c3')
            page_content = page.content()
            browser.close()


        soup = BeautifulSoup(page_content, "html.parser")
        target_text = re.compile(r'دانشکده‌ها')
        dropdown_elements = soup.find_all("li", class_="dropdown")
        for dropdown in dropdown_elements:
            anchor_tag = dropdown.find("a", class_="dropdown-toggle")
        
            if anchor_tag and target_text.search(anchor_tag.get_text(strip=True)):
                links = dropdown.find_all("a")[1:]
                for link in links:
                    href = link.get("href")
                    text = link.get_text(strip=True)

                    if href and text:
                        college = CollegeData(href=href, value=text)
                        yield college

    def get_professors(self):
        pass

    def get_professor_page(self, link) -> Professor:
        pass

    def get_employee_page(self) -> Employee:
        return super().get_employee_page()

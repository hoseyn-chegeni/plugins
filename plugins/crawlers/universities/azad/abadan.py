from bs4 import BeautifulSoup
from crawlers.universities.base import University
from schemas.employee import Employee
from playwright.sync_api import sync_playwright
from schemas.colleges import CollegeData
from schemas.professor import (
    Professor,
)
import re


class AbadanCrawler(University):
    def __init__(self) -> None:
        self.url = "https://abadan.iau.ir/"

    def get_employees(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://abadan.iau.ir/fa/grid/4/%D8%B1%D8%A7%D9%87%D9%86%D9%85%D8%A7%DB%8C-%D8%AC%D8%A7%D9%85%D8%B9-%D8%AA%D9%84%D9%81%D9%86-%D9%87%D8%A7%DB%8C-%D9%88%D8%A7%D8%AD%D8%AF?GridSearch%5BpageSize%5D=200&GridSearch%5Bsearch%5D=")
            page.wait_for_selector('table.table-striped')
            page_content = page.content()
            browser.close()


        soup = BeautifulSoup(page_content, "html.parser")
        table = soup.find('table', class_='table-striped')
        table_data = []
        rows = table.find('tbody').find_all('tr')
        for row in rows:

            columns = row.find_all('td')

            first_name = columns[1].get_text(strip=True)
            last_name = columns[2].get_text(strip=True)
            role = columns[3].get_text(strip=True)
            dept = columns[4].get_text(strip=True)
            internal= columns[5].get_text(strip=True)
            phone_number = columns[6].get_text(strip=True)

            employee = Employee(name= first_name + " " + last_name, role=role, department= dept, phone_number= phone_number, internal_number= internal)
            
            yield employee

    def get_colleges(self):
        pass

    def get_professors(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://abadan.iau.ir/fa/faculty/faculty-list/2#18")
            page.wait_for_selector('.col-xs-8') 
            page_content = page.content()
            browser.close()

        soup = BeautifulSoup(page_content, "html.parser")
        faculty_divs = soup.find_all('div', class_='col-xs-8')
        for faculty in faculty_divs:
            name_tag = faculty.find('h4', class_='heading')
            if name_tag:
                name = name_tag.get_text(strip=True)
            position_tag = faculty.find('i', class_='fa-graduation-cap')
            if position_tag:
                position_text = position_tag.next_sibling.strip() if position_tag.next_sibling else None
                rank = position_text

            resume_link = faculty.find('a', href=re.compile(r'\.pdf$'))
            if resume_link:
                resume_url = resume_link['href']
            professor = Professor(full_name= name, rank= rank)
            professor.socials.personal_cv = resume_url
            yield professor

        

    def get_professor_page(self, link) -> Professor:
        pass

    def get_employee_page(self) -> Employee:
        return super().get_employee_page()

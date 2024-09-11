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
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            base_url = "https://ntb.iau.ir/fa/grid/40/%D8%AF%D9%81%D8%AA%D8%B1-%D8%AA%D9%84%D9%81%D9%86-%D8%AC%D8%AF%DB%8C%D8%AF?GridSearch%5BpageSize%5D=200&GridSearch%5Bsearch%5D=&page="
            page_num = 1
            previous_first_row = None

            while True:
                url = f"{base_url}{page_num}&per-page=200"
                page.goto(url)
                page.wait_for_selector("td")  # Ensure the page content is loaded
                page_content = page.content()
                soup = BeautifulSoup(page_content, "html.parser")

                # Find all the relevant table rows
                tr_elements = soup.find_all("tr", class_="")  # Match the tr elements that have no class

                all_rows = []
                # Extract data row by row
                for tr in tr_elements:
                    # Find all td elements within the tr
                    td_elements = tr.find_all("td")
                    
                    if td_elements:  # Only proceed if td elements are found
                        # Map the correct fields from the table, using data-title attribute
                        name = td_elements[0].get_text(strip=True)
                        internal_number = td_elements[1].get_text(strip=True)
                        role = td_elements[2].get_text(strip=True)
                        department = td_elements[3].get_text(strip=True)

                        # Store the employee data
                        employee = Employee(
                            name=name,
                            internal_number=internal_number,
                            role=role,
                            department=department
                        )
                        yield employee

                if not tr_elements or (previous_first_row and tr_elements[0] == previous_first_row):
                    break
                
                previous_first_row = tr_elements[0]  # Set the first row for comparison in the next page
                page_num += 1

            browser.close()

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

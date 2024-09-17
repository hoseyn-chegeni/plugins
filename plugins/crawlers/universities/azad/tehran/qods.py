from crawlers.universities.base import University
from schemas.employee import Employee
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from schemas.professor import Professor


class QodsCrawler(University):
    def __init__(self) -> None:
        self.url = ""

    def get_employees(self):
        pass

    def get_colleges(self):
        pass

    def get_professors(self):
        base_url = "https://qods.iau.ir/fa/faculty?page={}"
        page_number = 1
        last_page_data = None
        all_professors_data = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            while True:
                page.goto(base_url.format(page_number))
                page.wait_for_selector("tbody")
                page_content = page.content()
                soup = BeautifulSoup(page_content, "html.parser")
                tbody = soup.find("tbody")
                rows = tbody.find_all("tr")
    
                current_page_data = []
                
                for row in rows:
                    
                    # Extract information from the table cells
                    profile_img = row.find("img")["src"] if row.find("img") else None
                    last_name = row.find("td", {"data-title": "نام خانوادگی"}).get_text(strip=True)
                    first_name = row.find("td", {"data-title": "نام"}).get_text(strip=True)
                    faculty_group = row.find("td", {"data-title": "دانشکده/گروه"}).get_text(strip=True)
                    rank = row.find("td", {"data-title": "رتبه"}).get_text(strip=True)
                    
                    
                    # CV download link
                    cv_link_tag = row.find("a", {"href": lambda href: href and href.endswith(".pdf")})
                    cv_link = cv_link_tag["href"] if cv_link_tag else None
                    
                    # Profile link
                    
                    professor = Professor(full_name= first_name + ' ' + last_name, faculty= faculty_group, rank= rank, image= profile_img)
                    professor.socials.personal_cv = cv_link
                    yield professor
                    current_page_data.append({
                        "first_name": first_name,
                        "last_name": last_name,
                        "profile_img": profile_img,
                    })
            
                if current_page_data == last_page_data:
                    break
                
                all_professors_data.extend(current_page_data)
                last_page_data = current_page_data
                
                page_number += 1

            browser.close()    


    def get_professor_page(self):
        return super().get_professor_page()

    def get_employee_page(self) -> Employee:
        return super().get_employee_page()

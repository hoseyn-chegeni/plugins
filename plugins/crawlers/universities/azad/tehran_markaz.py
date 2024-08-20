from bs4 import BeautifulSoup
from crawlers.universities.base import University
from schemas.employee import Employee
from playwright.sync_api import sync_playwright
from schemas.colleges import CollegeData
from schemas.professor import Professor
from crawlers.universities.azad.groups import get_professors_1, get_professors_2,get_professors_3, get_professors_4, get_professors_5, get_professors_6, get_professors_7, get_professors_8, get_professors_9

class TehranMarkazCrawler(University):
    def __init__(self) -> None:
        self.url = "https://ctb.iau.ir"

    def get_employees(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            base_url = "https://ctb.iau.ir/fa/grid/16/%D8%A7%D8%B7%D9%84%D8%A7%D8%B9%D8%A7%D8%AA-%D8%AA%D9%85%D8%A7%D8%B3?GridSearch%5BpageSize%5D=200&GridSearch%5Bsearch%5D=&page="
            page_num = 1
            previous_first_row = None

            while True:
                url = f"{base_url}{page_num}&per-page=200"
                page.goto(url)
                page.wait_for_selector("td")
                page_content = page.content()
                soup = BeautifulSoup(page_content, "html.parser")
                tr_elements = soup.find_all("tr")
                all_rows = []
                for tr in tr_elements:
                    td_elements = tr.find_all("td")
                    row = [td.get_text(strip=True) for td in td_elements]
                    if row and not row[0] == "":
                        all_rows.append(row)
                if all_rows:
                    current_first_row = all_rows[0]
                    if previous_first_row and current_first_row == previous_first_row:
                        break
                    for row in all_rows:
                        employee = Employee(
                            name=row[1],
                            role=row[2],
                            department=row[3],
                            internal_number=row[4],
                            phone_number=row[5],
                        )
                        yield employee
                    previous_first_row = current_first_row
                else:
                    break
                page_num += 1
            browser.close()

    def get_colleges(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://ctb.iau.ir/fa")
            page.wait_for_selector("ul#wb08a2d9f4c3791de4252d29fb27982a15")
            page_content = page.content()
            browser.close()
            soup = BeautifulSoup(page_content, "html.parser")
            ul_element = soup.find("ul", id="wb08a2d9f4c3791de4252d29fb27982a15")
            links = ul_element.find_all("a")
            for link in links[1:]:
                href = link.get("href")
                if not href.startswith("http"):
                    href = "https://ctb.iau.ir" + href
                college = CollegeData(href=href, value=link.text.strip())
                yield college


    def get_professors(self):
        # ادبیات علوم انسانی -علوم قرآن و حدیث
        for professor in get_professors_1():
            yield professor

        # ادبیات علوم انسانی -   ادیان و عرفان اسلامی
        for professor in get_professors_2():
            yield professor

        # ادبیات علوم انسانی -   فقه و حقوق اسلامی
        for professor in get_professors_3():
            yield professor

        # ادبیات علوم انسانی -  تاریخ و باستانشناسی
        for professor in get_professors_4():
            yield professor

        # ادبیات علوم انسانی - فلسفه و حکمت اسلامی
        for professor in get_professors_5():
            yield professor

        # ادبیات علوم انسانی - فلسفه غرب
        for professor in get_professors_6():
            yield professor      

        # ادبیات علوم انسانی -  جغرافیا
        for professor in get_professors_7():
            yield professor   
               
        # ادبیات علوم انسانی -  زبان و ادبیات فارسی
        for professor in get_professors_8():
            yield professor

        # ادبیات علوم انسانی - زبان و ادبیات عرب
        for professor in get_professors_9():
            yield professor

    def get_professor_page(self) -> Professor:
        return super().get_professor_page()

    def get_employee_page(self) -> Employee:
        return super().get_employee_page()

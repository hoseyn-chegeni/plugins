import requests
from bs4 import BeautifulSoup
from schemas import colleges
from crawlers.universities.base import University
from crawlers.utils import check_connection
from schemas import Course, Professor, Skill, Book, Honor
from schemas.employee import Employee
import xml.etree.ElementTree as ET
from typing import Generator
import re


class ElmSanatCrawler(University):
    def __init__(self) -> None:
        self.url = "https://www.iust.ac.ir/"
        self.it_url = "https://its.iust.ac.ir/api/its/profsprofilelist"
        self.phone_book_url = "https://its.iust.ac.ir/phonebook/view"

    def get_employees(self):
        session = requests.Session()
        response = check_connection(requests.get, self.phone_book_url)
        soup = BeautifulSoup(response.content, "html.parser")
        form = soup.find("form", id="phonebook-searchform")
        form_build_id = form.find("input", {"name": "form_build_id"})["value"]
        form_id = form.find("input", {"name": "form_id"})["value"]
        select = form.find("select", {"name": "vid"})
        options = select.find_all("option")

        for option in options:
            option_value = option["value"]
            option_text = option.text
            form_data = {
                "lastname": "",
                "vid": option_value,
                "form_build_id": form_build_id,
                "form_id": form_id,
                "search": "جستجو",
            }
            response = session.post(self.phone_book_url, data=form_data)
            result_soup = BeautifulSoup(response.content, "html.parser")
            table = result_soup.find(
                "table", {"class": "table table-bordered table-hover rtecenter"}
            )

            if table:
                rows = table.find("tbody").find_all("tr")
                print(f"Results for {option_text}:")
                for row in rows:
                    columns = row.find_all("td")
                    name = columns[0].text.strip()
                    unit = columns[1].text.strip()
                    phone = columns[2].text.strip()
                    fax = columns[3].text.strip() if len(columns) > 3 else ""

                    if re.match(r"^(آقای|خانم|دکتر)", name):
                        employee = Employee(
                            department=unit,
                            name=name,
                            internal_number=phone,
                            phone_number=fax,
                        )
                        yield employee

    def get_colleges(self) -> Generator[colleges.CollegeData, None, None]:
        response = check_connection(
            requests.get, self.url + "persons.php?slc_lang=fa&sid=1&list_sections=1/fa/"
        )
        soup = BeautifulSoup(response.text, "html.parser")
        menu_section = soup.find("ul", class_="dropdown-menu mega-dropdown-menu row")
        if not menu_section:
            return

        for a_tag in menu_section.find_all("a", href=True):
            text_value = a_tag.get_text(strip=True)
            if re.match(r"^دانشکده", text_value):
                yield colleges.CollegeData(
                    href=self.url + a_tag["href"], value=text_value
                )

    def get_professors(self):
        response = check_connection(requests.post, self.it_url)
        root = ET.fromstring(response.content)
        for item in root.findall(".//item"):
            link = item.find("profile").text
            yield link

    def get_professor_page(self, link: str):
        response = check_connection(requests.get, link)
        soup = BeautifulSoup(response.text, "html.parser")
        rows_value = []
        college = None
        specializations = []
        teachings = []

        rows = soup.find_all("td")
        for i in rows:
            rows_value.append(i.text)
            if "دانشکده" in i.text:
                college = i.text

        professor = Professor(
            full_name=soup.find("h1", style="font-size:1.5em").text.strip(),
            rank=rows_value[0],
            college=college,
        )
        #SOCIALS 
        try:
            email_span = soup.find('span', class_='email', style="font-size:9.0pt;", dir="RTL")
            if email_span:
                email_text = email_span.text.strip()
                professor.email = email_text.split(':')[-1].strip()
        except:
            pass
        try:
            span_elements = soup.find_all('span', style="font-size:9.0pt;")
            for span_element in span_elements:
                span_text = span_element.text.strip()
                match = re.search(r'تلفن دانشگاه: (\d+)', span_text)
                if match:
                    professor.phone_number = match.group(1)
        except:
            pass
        try:
            scholar_links = soup.find_all('a', href=True)
            for link in scholar_links:
                if link.find('span', string=lambda x: x and 'Google Scholar' in x):
                    professor.socials.scholar = link['href']
                    break

        except:
            pass
        try:
            google = soup.find_all('a', href=True)
            for link in google:
                if link.find('span', string=lambda x: x and 'Home Page' in x):
                    professor.socials.google = link['href']
                    break
        except:
            pass
        try:
            scopus = soup.find_all('a', href=True)
            for link in scopus:
                if link.find('span', string=lambda x: x and 'Scopus' in x):
                    professor.socials.scopus = link['href']
                    break
        except:
            pass
        try:
            span_elements = soup.find_all('span', style="font-size:9.0pt;")
            for span_element in span_elements:
                span_text = span_element.text.strip()
                match = re.search(r'همراه: (\+\d+)', span_text)
                if match:
                    professor.socials.telegram = match.group(1)        
        except:
            pass

        # HONOR
        honors_list = []
        honor_elements = soup.find_all(
            "div", class_="col-lg-12 col-md-12 col-sm-12 col-xs-12 text-right"
        )

        for honor_element in honor_elements:
            honor_tables = honor_element.find_all(
                "table", class_="table table-hover table-bordered"
            )

            for honor_table in honor_tables:
                headers = honor_table.find_all("th")
                header_titles = [header.text.strip() for header in headers]

                if (
                    "ردیف" in header_titles
                    and "عنوان" in header_titles
                    and "سال" in header_titles
                ):
                    rows = honor_table.find("tbody").find_all("tr")

                    r_index = header_titles.index("ردیف")
                    for row in rows:
                        cells = row.find_all("td")
                        row_data = [
                            cell.text.strip()
                            for idx, cell in enumerate(cells)
                            if idx != r_index
                        ]
                        honors_list.append(row_data)
        try:
            for i in honors_list:
                professor.honors.append(Honor(title=i[0], date=i[1]))
        except:
            pass

        # BOOKS
        book_table = soup.find(
            "table", {"class": "table table-hover table-bordered align-middle"}
        )
        if book_table:
            headers = [header.text for header in book_table.find_all("th")]
            rows = []
            for row in book_table.find_all("tr")[1:]:  # Skip the header row
                cells = [cell.text.strip() for cell in row.find_all("td")]
                rows.append(cells)
            books = [row for row in rows]
        try:
            for book in books:
                if len(book) >= 4:
                    authors = [author.strip() for author in book[3].split(",")]
                    new_book = Book(
                        publish_date=book[0], title=book[2], authors=authors
                    )
                    professor.books.append(new_book)
        except:
            pass

        # COURSES AND SKILLS
        table = soup.find("table", {"class": "table table-hover table-bordered"})
        if table:
            headers = table.find("thead").find_all("th")
            columns = {
                header.get_text(strip=True): idx for idx, header in enumerate(headers)
            }
            if "زمینه های تخصصی" in columns or "دروس تدریسی" in columns:
                specialization_idx = columns["زمینه های تخصصی"]
                teaching_idx = columns["دروس تدریسی"]
                rows = table.find("tbody").find_all("tr")
                for row in rows:
                    cells = row.find_all("td")
                    if len(cells) > specialization_idx and len(cells) > teaching_idx:
                        specializations.append(
                            cells[specialization_idx].get_text(strip=True)
                        )
                        teachings.append(cells[teaching_idx].get_text(strip=True))
        try:
            for i in range(len(teachings)):
                professor.courses.append(
                    Course(description=None, period=None, title=teachings[i])
                )
        except:
            pass
        try:
            for i in range(len(specializations)):
                professor.skills.append(
                    Skill(start_date=None, title=specializations[i])
                )
        except:
            pass

        yield professor

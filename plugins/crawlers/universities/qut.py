import requests
from bs4 import BeautifulSoup
from schemas.colleges import CollegeData
from crawlers.universities.base import University
from crawlers.utils import check_connection
from schemas.professor import Professor,Book, EducationalRecord, Interest
from schemas.employee import Employee


class QUTCrawler(University):

    def __init__(self) -> None:
        self.url = "https://www.qut.ac.ir/"

    def get_employees(self):
        response = check_connection(
            requests.get, self.url + "/fa/publicrelations/persons"
        )
        soup = BeautifulSoup(response.content, "html.parser")
        rows = soup.find_all("tr", attrs={"data-original-title": ""})
        for row in rows:
            cells = row.find_all("td")
            for i in range(0, len(cells), 3):
                if i + 2 < len(cells):
                    name_cell = cells[i]
                    dept_cell = cells[i + 1]
                    phone_cell = cells[i + 2]

                    if (
                        "color: #ff0000;" not in str(name_cell.get("style", ""))
                        and "color: #ff0000;" not in str(dept_cell.get("style", ""))
                        and "color: #ff0000;" not in str(phone_cell.get("style", ""))
                    ):
                        name = name_cell.text.strip()
                        dept = dept_cell.text.strip()
                        phone = phone_cell.text.strip()
                        employee = Employee(
                            name=name, department=dept, internal_number=phone
                        )
                        yield employee

    def get_colleges(self):
        response = check_connection(requests.get, self.url + "/fa/wp/index")
        soup = BeautifulSoup(response.text, "html.parser")
        th_elements = soup.find_all("th", attrs={"data-original-title": ""})

        # Iterate through each <th> element to check the text
        for th in th_elements:
            th_text = th.text.strip()
            if th_text.startswith("لیست اعضای هیئت علمی"):
                result_text = th_text[len("لیست اعضای هیئت علمی ") :]
                college = CollegeData(value=result_text)
                return college

    def get_professors(self):
        response = check_connection(requests.get, self.url + "/fa/wp/index")
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all("tr", attrs={"data-original-title": ""})
        for row in rows:
            cells = row.find_all("td")
            if len(cells) == 7:
                name = cells[1].text.strip()
                college = cells[2].text.strip()
                title = cells[3].text.strip()

                personal_page_link = (
                    cells[4].find("a", href=True)["href"].strip()
                    if cells[4].find("a", href=True)
                    else None
                )
                google_scholar_link = (
                    cells[4].find_all("a", href=True)[1]["href"].strip()
                    if len(cells[4].find_all("a", href=True)) > 1
                    else None
                )
                scopus_link = (
                    cells[4].find_all("a", href=True)[2]["href"].strip()
                    if len(cells[4].find_all("a", href=True)) > 2
                    else None
                )

                email = cells[5].text.strip()
                image_src = (
                    self.url + cells[6].find("img")["src"].strip()
                    if cells[6].find("img")
                    else None
                )

                # If any element is None or empty, replace it with an empty list
                personal_page_link = (
                    self.url + personal_page_link if personal_page_link else None
                )
                google_scholar_link = (
                    google_scholar_link if google_scholar_link else None
                )
                scopus_link = scopus_link if scopus_link else None
                image_src = image_src if image_src else None

                professor = Professor(
                    full_name=name,
                    college=college,
                    rank=title,
                    email=email,
                    image=image_src,
                )
                professor.socials.scholar = google_scholar_link
                professor.socials.scopus = scopus_link
                professor.socials.personal_cv = personal_page_link

                if personal_page_link:
                    self.get_professor_page(professor, personal_page_link)



    def get_professor_page(self, professor, personal_page_link):
        response = check_connection(requests.get, personal_page_link)
        soup = BeautifulSoup(response.text, "html.parser")
        try:
            h2_element = soup.find('h2', {'data-original-title': '', 'title': ''})
            if h2_element:
                professor.full_name_en = h2_element.text.strip()
        except:
            pass
        try:
            p_elements = soup.find_all('p', {'data-original-title': '', 'title': ''})
            for p_element in p_elements:
                if "مقاله" in p_element.get_text() or"مقالات" in p_element.get_text():
                    ol_elements = p_element.find_next_siblings('ol', {'dir': 'ltr', 'data-original-title': '', 'title': ''})
                    for ol in ol_elements:
                        li_elements = ol.find_all('li')
                        for li in li_elements:
                            # Split text at the first semicolon to separate author(s) and title
                            parts = li.get_text(strip=True).split(",")
                            authors = parts[0].strip()
                            title = ",".join(parts[1:]).strip() if len(parts) > 1 else ""
                            new_book = Book(authors=[authors], title=title)
                            professor.books.append(new_book)
        except :
            pass


        try:
            elements = soup.find_all('p', text='تحصیلات:')
            for element in elements:
                ul = element.find_next_sibling('ul')
                if ul:
                    for li in ul.find_all('li'):
                       new_education_record =EducationalRecord(li.get_text(strip=True))
                       professor.educational_records.app(new_education_record)
        except:
            pass
        try:
            all_elements = soup.find_all(string=lambda text: "پژهش" in text)
            for element in all_elements:
                parent = element.find_parent('strong')
                if parent:
                    ol = parent.find_next_sibling("ol")
                    if ol:
                        for li in ol.find_all("li"):
                            interest =Interest(title= li.get_text(strip=True))
                            professor.interest.append(interest)
        except:
            pass
        
        return professor
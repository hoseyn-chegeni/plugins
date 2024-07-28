import requests
from bs4 import BeautifulSoup
from schemas import colleges
from crawlers.universities.base import University
from crawlers.utils import check_connection
from schemas import Course, Professor, Skill
from typing import List, Generator
import re
import xml.etree.ElementTree as ET



class ElmSanatCrawler(University):
    def __init__(self) -> None:
        self.url = "https://www.iust.ac.ir/"
        self.it_url = "https://its.iust.ac.ir/api/its/profsprofilelist"


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
        response = check_connection(requests.post, self.it_url )        
        root = ET.fromstring(response.content)
        for item in root.findall('.//item'):
            link = item.find('profile').text
            yield link


class ElmSanatCrawler(University):
    def __init__(self) -> None:
        self.url = "https://its.iust.ac.ir/api/its/profsprofilelist"

    def get_professors(self):
        response = check_connection(requests.post, self.url )        
        root = ET.fromstring(response.content)
        for item in root.findall('.//item'):
            link = item.find('profile').text
            yield link


    def get_professor_page(self, link: str):
        response = check_connection(requests.get, link)
        soup = BeautifulSoup(response.text, "html.parser")
        rows_value = []
        college = None
        specializations = []
        teachings = []
        table = soup.find('table', {'class': 'table table-hover table-bordered'})
        if table:
            headers = table.find('thead').find_all('th')
            columns = {header.get_text(strip=True): idx for idx, header in enumerate(headers)}
            if "زمینه های تخصصی"  in columns or "دروس تدریسی"  in columns:
                specialization_idx = columns["زمینه های تخصصی"]
                teaching_idx = columns["دروس تدریسی"]
                rows = table.find('tbody').find_all('tr')
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) > specialization_idx and len(cells) > teaching_idx:
                        specializations.append(cells[specialization_idx].get_text(strip=True))
                        teachings.append(cells[teaching_idx].get_text(strip=True))


        rows = soup.find_all('td')
        for i in rows:
            rows_value.append(i.text)
            if "دانشکده" in i.text:
                college = i.text


        professor = Professor(
            full_name= soup.find('h1', style="font-size:1.5em").text.strip(),
            rank= rows_value[0],
            college=college,
        )

        professor.email = soup.find('span', class_="email", style="font-size:9.0pt;", dir="RTL").text.strip()
        try:
            professor.phone_number = soup.find('span', style="font-size:9.0pt;").text.strip()
        except:
            pass
        try:
            scholar = soup.find('a', href=True, text=lambda x: x and 'Google Scholar' in x)
            if scholar:
                professor.socials.scholar = scholar['href']
        except:
            pass
        try:
            google = soup.find('a', href=True, text=lambda x: x and 'Home Page' in x)
            if google:
                professor.socials.google = google['href']
        except:
            pass
        try:     
            for i in range(len(teachings)):
                professor.courses.append(Course(description = None, period=None, title=teachings[i]))
        except:
            pass
        try:     
            for i in range(len(specializations)):
                professor.skills.append(Skill(start_date=None, title=specializations[i]))
        except:
            pass
        return professor
    

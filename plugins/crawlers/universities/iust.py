import requests
from bs4 import BeautifulSoup
from universities.base import University
from utils import check_connection
from typing import List, Generator
import re
from schemas import colleges
from schemas import professor as P


class ElmSanatCrawler(University):
    def __init__(self) -> None:
        self.url = "https://www.iust.ac.ir/"
        self.electrical_engineering = "https://ee.iust.ac.ir/"
        self.mechanical_engineering = "https://mech.iust.ac.ir/"
        self.automotive_engineering = "https://aed.iust.ac.ir/"
        self.railway_engineering = "https://railway.iust.ac.ir/"
        self.mathematics_and_computer_science = "https://math.iust.ac.ir/"
        self.chemistry = "https://chemistry.iust.ac.ir/"
        self.chemical_petroleum_and_gas_engineering = "http://chem_eng.iust.ac.ir/"
        self.industrial_engineering = "https://ie.iust.ac.ir/"
        self.civil_engineering = "https://civil.iust.ac.ir/"
        self.advanced_technologies = "https://fn.iust.ac.ir/"
        self.physics = "https://physics.iust.ac.ir/"
        self.computer_engineering = "https://ce.iust.ac.ir/"
        self.architecture_and_environmental_design = "https://www.iust.ac.ir/"
        self.economy = "https://pe.iust.ac.ir/"
        self.metallurgy_and_materials = "http://meteng.iust.ac.ir/"

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

    # دانشکده مهندسی برق
    def get_professors_electrical_engineering(self):
        response = check_connection(
            requests.get, self.electrical_engineering + "content/77541/اعضاء-هیات-علمی"
        )
        soup = BeautifulSoup(response.content, "html.parser")
        for teacher_info in soup.find_all("div", {"class": "teacher-description"}):
            link = teacher_info.find("a", href=True)["href"]
            yield link

    def get_electrical_engineering_professor_page(self, link: str):
        response = check_connection(requests.get, link)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def get_professors_mechanical_engineering(self):
        response = check_connection(
            requests.get, self.mechanical_engineering + "faculty/"
        )
        soup = BeautifulSoup(response.content, "html.parser")

# مهندسی خودرو
    def get_professors_automotive_engineering(self):
        response = check_connection(
            requests.get, self.automotive_engineering + "page/13939/اعضاء-هیات-علمی"
        )
        soup = BeautifulSoup(response.content, "html.parser")
        divs = soup.find_all("div", style="text-align: center;")
        for div in divs:
            links = div.find_all('a')
            detail_link = None
            for link in links:
                href = link.get('href')
                if href and re.match(r'^http://scimet.iust', href):
                    detail_link = href
                    if detail_link is not None:
                        yield detail_link
                        

    def get_automotive_engineering_professor_page(self, link: str):
        response = check_connection(requests.get, link)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    # دانشکده مهندسی راه آهن
    def get_professors_railway_engineering(self):
        response = check_connection(
            requests.get, self.railway_engineering + "page/913/اساتید"
        )
        soup = BeautifulSoup(response.content, "html.parser")
        divs = soup.find_all("div", class_="rounded")

        for div in divs:
            name_tag = div.find("a")
            link = (
                self.railway_engineering + name_tag["href"]
                if name_tag and name_tag["href"]
                else None
            )
            if link is not None:
                yield link

    def get_railway_professor_page(self, link: str):
        response = check_connection(requests.get, link)
        soup = BeautifulSoup(response.text, "html.parser")


#ریاضی 

    def get_professors_mathematics_and_computer_science(self):
        response = check_connection(
            requests.get,
            self.mathematics_and_computer_science + "page/19620/اعضای-هیئت-علمی",
        )
        soup = BeautifulSoup(response.content, "html.parser")
        divs = soup.find_all('div', style="text-align: center;")
        for div in divs:
            link = div.find('a', href=True)
            if link and link['href'].startswith("http://math.iust.ac.ir"):
                yield link
    def get_mathematics_and_computer_science_professor_page(self, link: str):
        response = check_connection(requests.get, link)
        soup = BeautifulSoup(response.text, "html.parser")
        professor_info = {}

        # Extract professor's name
        name_element = soup.select_one("td[rowspan='1'] span strong")
        if name_element:
            professor_info['name'] = name_element.get_text(strip=True)
        
        # Extract email, phone, fax, postal code, address, and website
        contact_info_element = soup.select_one("td img[alt=''][src*='mail-iust-36x36.png']")
        if contact_info_element:
            contact_info_td = contact_info_element.find_parent("td")
            contact_info = contact_info_td.get_text(separator="\n", strip=True)
            lines = contact_info.split("\n")
            
            if len(lines) > 1:
                professor_info['email'] = lines[1].split(":", 1)[1].strip() if ":" in lines[1] else ""
            if len(lines) > 3:
                professor_info['phone'] = lines[3].split(":", 1)[1].strip() if ":" in lines[3] else ""
            if len(lines) > 5:
                professor_info['fax'] = lines[5].split(":", 1)[1].strip() if ":" in lines[5] else ""
            if len(lines) > 7:
                professor_info['postal_code'] = lines[7].split(":", 1)[1].strip() if ":" in lines[7] else ""
            if len(lines) > 9:
                professor_info['address'] = lines[9].split(":", 1)[1].strip() if ":" in lines[9] else ""
            if len(lines) > 11:
                professor_info['website'] = lines[11].split(":", 1)[1].strip() if ":" in lines[11] else ""
        
        # Extract virtual lab and research lab info
        labs_element = soup.select_one("td img[alt=''][src*='faculty-mech-iust-icon.png']")
        if labs_element:
            labs_td = labs_element.find_parent("td")
            labs_info = labs_td.get_text(separator="\n", strip=True)
            labs_lines = labs_info.split("\n")
            
            if len(labs_lines) > 0:
                professor_info['virtual_lab'] = labs_lines[0].split(":", 1)[1].strip() if ":" in labs_lines[0] else ""
            if len(labs_lines) > 2:
                professor_info['research_lab'] = labs_lines[2].split(":", 1)[1].strip() if ":" in labs_lines[2] else ""
        


    # دانشکده مهندسی شیمی
    def get_professors_chemistry(self):
        response = check_connection(
            requests.get, self.chemistry + "page/20311/اعضای-هیات-علمی"
        )
        soup = BeautifulSoup(response.content, "html.parser")
        for teacher_info in soup.find_all("div", {"class": "teacher-description"}):
            link = teacher_info.find("a", href=True)["href"]
            yield link

    def get_chemistry_professor_page(self, link: str):
        response = check_connection(requests.get, link)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    # مهندسی شیمی نفت و گاز
    def get_professors_chemical_petroleum_and_gas_engineering(self):
        response = check_connection(
            requests.get, self.chemical_petroleum_and_gas_engineering + "faculty/"
        )
        soup = BeautifulSoup(response.content, "html.parser")
        for teacher_info in soup.find_all(
            "div",
            {
                "class": "w-post-elm post_custom_field usg_post_custom_field_1 type_text fjb_faculty_info color_link_inherit"
            },
        ):
            link = teacher_info.find("a", href=True)["href"]
            yield self.chemical_petroleum_and_gas_engineering + link

    def get_chem_eng_professor_page(self, link: str):
        response = check_connection(requests.get, link)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    # مهندسی صنایع
    def get_professors_industrial_engineering(self):
        response = check_connection(
            requests.get, self.industrial_engineering + "page/5318/اعضاء-هیات-علمی"
        )
        soup = BeautifulSoup(response.text, "html.parser")
        for td in soup.find_all("td", class_="tbld_odd"):
            name_anchor = td.find("a")
            if name_anchor:
                yield (
                    self.industrial_engineering + name_anchor["href"]
                    if name_anchor.has_attr("href")
                    else None
                )

    def get_ie_professor_page(self, link: str):
        response = check_connection(requests.get, link)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def get_professors_civil_engineering(self):
        response = check_connection(
            requests.get, self.civil_engineering + "page/5991/اعضاء-هیأت-علمی"
        )
        soup = BeautifulSoup(response.content, "html.parser")

    # فناوری های نوین
    def get_professors_advanced_technologies(self):
        response = check_connection(
            requests.get, self.advanced_technologies + "page/20260/اعضای-هیات-علمی"
        )
        soup = BeautifulSoup(response.content, "html.parser")
        for teacher_info in soup.find_all("div", {"class": "teacher-description"}):
            link = teacher_info.find("a", href=True)["href"]
            yield link

    def get_advanced_technologies_professor_page(self, link: str):
        response = check_connection(requests.get, link)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    # فیزیک
    def get_professors_physics(self):
        response = check_connection(requests.get, self.physics + "faculty/")
        soup = BeautifulSoup(response.content, "html.parser")
        elements = soup.find_all(
            "a",
            class_="btn btn-style-3d btn-style-semi-round btn-size-small btn-scheme-inherit btn-scheme-hover-inherit btn-icon-pos-right",
        )

        for element in elements:
            link = element["href"]
            yield link

    def get_physics_faculty_professor_page(self, link: str):
        response = check_connection(requests.get, link)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    #  مهندسی کامپیوتر
    def get_professors_computer_engineering(self):
        response = check_connection(
            requests.get,
            self.computer_engineering + "page/18766/اعضا-هیات-علمی-در-یک-نگاه",
        )
        soup = BeautifulSoup(response.content, "html.parser")
        for link in soup.find_all("a", href=True):
            if "content" in link["href"]:
                yield link["href"]

    def get_computer_engineering_professor_page(self, link: str):
        response = check_connection(requests.get, link)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    # شهر سازی
    def get_professors_architecture_and_environmental_design(self):
        response = check_connection(
            requests.get,
            self.architecture_and_environmental_design
            + "page/7134/%D8%A7%D8%B9%D8%B6%D8%A7%DB%8C-%D9%87%DB%8C%D8%A6%D8%AA-%D8%B9%D9%84%D9%85%DB%8C",
        )
        soup = BeautifulSoup(response.content, "html.parser")
        for td in soup.find_all("td", style="text-align: center;"):
            a_tag = td.find("a")
            if a_tag:
                span_tag = a_tag.find("span", style="font-size:11px;")
                if span_tag:
                    link = a_tag["href"]
                    yield link

    def get_aed_professor_page(self, link: str):
        response = check_connection(requests.get, link)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    # اقتصاد
    def get_professors_economy(self):
        response = check_connection(
            requests.get, self.economy + "page/11376/اعضای-هیأت-علمی"
        )
        soup = BeautifulSoup(response.content, "html.parser")
        for teacher_info in soup.find_all("div", {"class": "teacher-description"}):
            link = teacher_info.find("a", href=True)["href"]
            yield link

    def get_economy_professor_page(self, link: str):
        response = check_connection(requests.get, link)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def get_professors_metallurgy_and_materials(self):
        response = check_connection(
            requests.get, self.metallurgy_and_materials + "faculty/"
        )
        soup = BeautifulSoup(response.content, "html.parser")

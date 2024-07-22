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
        self.architecture_and_environmental_design = "https://www.iust.ac.ir/index.php?sid=27&slc_lang=fa"
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
        response = check_connection(requests.get, self.electrical_engineering + "content/77541/اعضاء-هیات-علمی")
        soup = BeautifulSoup(response.content, "html.parser")
        for teacher_info in soup.find_all("div", {"class": "teacher-description"}):
            link = teacher_info.find("a", href=True)["href"]
            yield link


    def get_electrical_engineering_professor_page(self, link: str):
        response = check_connection(requests.get, link)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup


    def get_professors_mechanical_engineering(self):
        response = check_connection(requests.get, self.mechanical_engineering + "faculty/")
        soup = BeautifulSoup(response.content, "html.parser")


    def get_professors_automotive_engineering(self, link: str):
        response = check_connection(requests.get, self.automotive_engineering + "page/13939/اعضاء-هیات-علمی")
        soup = BeautifulSoup(response.content, "html.parser")

# دانشکده مهندسی راه آهن
    def get_professors_railway_engineering(self, link: str):
        response = check_connection(requests.get, self.railway_engineering + "page/913/اساتید")
        soup = BeautifulSoup(response.content, "html.parser")
        for teacher_info in soup.find_all("div", {"class": "rounded"}, style=True):
            link = teacher_info.find("a", href=True)["href"]
            yield self.railway_engineering + link

    def get_railway_professor_page(self, link: str):
        response = check_connection(requests.get, link)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup



    def get_professors_mathematics_and_computer_science(self, link: str):
        response = check_connection(requests.get, self.mathematics_and_computer_science + "page/19620/اعضای-هیئت-علمی")
        soup = BeautifulSoup(response.content, "html.parser")


# دانشکده مهندسی شیمی
    def get_professors_chemistry(self, link: str):
        response = check_connection(requests.get, self.chemistry + "page/20311/اعضای-هیات-علمی")
        soup = BeautifulSoup(response.content, "html.parser")
        for teacher_info in soup.find_all("div", {"class": "teacher-description"}):
            link = teacher_info.find("a", href=True)["href"]
            yield link

    def get_chemistry_professor_page(self, link: str):
        response = check_connection(requests.get, link)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

# مهندسی شیمی نفت و گاز     
    def get_professors_chemical_petroleum_and_gas_engineering(self, link: str):
        response = check_connection(requests.get, self.chemical_petroleum_and_gas_engineering + "faculty/")
        soup = BeautifulSoup(response.content, "html.parser")
        for teacher_info in soup.find_all("div", {"class": "w-post-elm post_custom_field usg_post_custom_field_1 type_text fjb_faculty_info color_link_inherit"}):
            link = teacher_info.find("a", href=True)["href"]
            yield self.chemical_petroleum_and_gas_engineering + link

    def get_chem_eng_professor_page(self, link: str):
        response = check_connection(requests.get, link)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    


    # مهندسی صنایع
    def get_professors_industrial_engineering(self, link: str):
        response = check_connection(requests.get, self.industrial_engineering + "page/5318/اعضاء-هیات-علمی")
        soup = BeautifulSoup(response.text, "html.parser")
        for teacher_info in soup.find_all("td", {"class": "tbld_odd"}):
            link = teacher_info.find("a", href=True)["href"]
            yield self.industrial_engineering + link

    def get_ie_professor_page(self, link: str):
        response = check_connection(requests.get, link)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    
       

    def get_professors_civil_engineering(self, link: str):
        response = check_connection(requests.get, self.civil_engineering + "page/5991/اعضاء-هیأت-علمی")
        soup = BeautifulSoup(response.content, "html.parser")



# فناوری های نوین
    def get_professors_advanced_technologies(self, link: str):
        response = check_connection(requests.get, self.advanced_technologies + "page/20260/اعضای-هیات-علمی")
        soup = BeautifulSoup(response.content, "html.parser")
        for teacher_info in soup.find_all("div", {"class": "teacher-description"}):
            link = teacher_info.find("a", href=True)["href"]
            yield link

    def get_dvanced_technologies_professor_page(self, link: str):
        response = check_connection(requests.get, link)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup


# فیزیک 
    def get_professors_physics(self, link: str):
        response = check_connection(requests.get, self.physics + "faculty/")
        soup = BeautifulSoup(response.content, "html.parser")
        for button_wrapper in soup.find_all("div", {"class": "wd-button-wrapper text-center"}):
            link = button_wrapper.find("a", href=True)["href"]
            yield link

    def get_physics_faculty_professor_page(self, link: str):
        response = check_connection(requests.get, link)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    
#  مهندسی کامپیوتر
    def get_professors_computer_engineering(self, link: str):
        response = check_connection(requests.get, self.computer_engineering + "page/18766/اعضا-هیات-علمی-در-یک-نگاه")
        soup = BeautifulSoup(response.content, "html.parser")
        for link in soup.find_all("a", href=True):
            if "content" in link["href"]:
                yield link["href"]

    def get_computer_engineering_professor_page(self, link: str):
        response = check_connection(requests.get, link)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup



# شهر سازی
    def get_professors_architecture_and_environmental_design(self, link: str):
        response = check_connection(requests.get, self.architecture_and_environmental_design + "page/7134/اعضای-هیئت-علمی")
        soup = BeautifulSoup(response.content, "html.parser")
        for td in soup.find_all("td", style="text-align: center;"):
            link = td.find("a", href=True)["href"]
            yield link

    def get_aed_professor_page(self, link: str):
        response = check_connection(requests.get, link)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup


# اقتصاد
    def get_professors_economy(self, link: str):
        response = check_connection(requests.get, self.economy + "page/11376/اعضای-هیأت-علمی")
        soup = BeautifulSoup(response.content, "html.parser")
        for teacher_info in soup.find_all("div", {"class": "teacher-description"}):
            link = teacher_info.find("a", href=True)["href"]
            yield link


    def get_economy_professor_page(self, link: str):
        response = check_connection(requests.get, link)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup



    def get_professors_metallurgy_and_materials(self, link: str):
        response = check_connection(requests.get, self.metallurgy_and_materials + "faculty/")
        soup = BeautifulSoup(response.content, "html.parser")
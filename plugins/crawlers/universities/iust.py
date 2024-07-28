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

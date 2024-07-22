import requests
from bs4 import BeautifulSoup
from universities.base import University
from utils import check_connection
from typing import List, Generator
import re
from schemas import colleges


class ElmSanatCrawler(University):
    def __init__(self) -> None:
        self.url = "https://www.iust.ac.ir/"

    def get_colleges(self) -> Generator[colleges.CollegeData, None, None]:
        response = check_connection(requests.get, self.url + "persons.php?slc_lang=fa&sid=1&list_sections=1/fa/")
        soup = BeautifulSoup(response.text, 'html.parser')
        menu_section = soup.find('ul', class_='dropdown-menu mega-dropdown-menu row')
        if not menu_section:
            return

        for a_tag in menu_section.find_all('a', href=True):
            text_value = a_tag.get_text(strip=True)
            if re.match(r'^دانشکده', text_value):
                yield colleges.CollegeData(href=self.url + a_tag['href'], value=text_value)

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


class QUTCrawler(University):

    def __init__(self) -> None:
        self.url = "https://www.qut.ac.ir/"


    def get_employees(self):
        pass

    def get_colleges(self):
        pass

    def get_professors(self):
        response = check_connection(requests.get, self.url + '/fa/wp/index' )
        soup = BeautifulSoup(response.text, "html.parser")
        for a_tag in soup.find_all('a', href=True, text='صفحه شخصی'):
            link = self.url + a_tag['href']
            yield link

    def get_professor_page(self, link: str):
        pass

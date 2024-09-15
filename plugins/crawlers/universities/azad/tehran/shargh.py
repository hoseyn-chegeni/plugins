from bs4 import BeautifulSoup
from crawlers.universities.base import University
from schemas.employee import Employee
from playwright.sync_api import sync_playwright
from schemas.colleges import CollegeData
from schemas.professor import (
    Professor,
    EducationalRecord,
    JobExperience,
    Activity,
    Honor,
)
from crawlers.universities.azad.groups.tehran_shargh import (
    get_shimi_prof,
    get_oloom_paye_prof,
    get_zist_prof,
    get_mohandesi_pezeshki_prof,
    get_computer_prof,
    get_omran_prof,
)


class TehranSharghCrawler(University):
    def __init__(self) -> None:
        self.url = "https://etb.iau.ir/"

    def get_employees(self):
        pass

    def get_colleges(self):
        pass

    def get_professors(self):
        # شیمی
        for professor in get_shimi_prof():
            yield professor
        # علوم پایه
        for professor in get_oloom_paye_prof():
            yield professor
        # زیست
        for professor in get_zist_prof():
            yield professor

        # مهندسی پزشکی
        for professor in get_mohandesi_pezeshki_prof():
            yield professor


        # کامپیوتر
        for professor in get_computer_prof():
            yield professor

        # مهندسی عمران 
        for professor in get_omran_prof():
            yield professor



    def get_professor_page(self) -> Professor:
        return super().get_professor_page()

    def get_employee_page(self) -> Employee:
        return super().get_employee_page()

import requests
from bs4 import BeautifulSoup
from schemas.colleges import CollegeData
from crawlers.universities.base import University
from crawlers.utils import check_connection
from schemas.professor import Professor, Book, EducationalRecord, Interest
from schemas.employee import Employee


class ChamranAhvazCrawler(University):

    def __init__(self) -> None:
        self.url = "https://scu.ac.ir/"

        self.headers = {
            "accept": "application/json, text/javascript, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "connection": "keep-alive",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cookie": "COOKIE_SUPPORT=true; JSESSIONID=D1D61BE0083B4405E7BEE4C9850E1712; __utma=135914867.1986027554.1722844427.1722844427.1722859103.2; __utmc=135914867; __utmz=135914867.1722859103.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; GUEST_LANGUAGE_ID=fa_IR; GUEST_LANGUAGE_ID_26011=fa_IR; __utmb=135914867.3.10.1722859103",
            "origin": "https://scu.ac.ir",
            "pragma": "no-cache",
            "referer": "https://scu.ac.ir/%D8%AA%D9%85%D8%A7%D8%B3-%D8%A8%D8%A7-%D8%AF%D8%A7%D9%86%D8%B4%DA%AF%D8%A7%D9%87",
            "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }

        self.payload = {
            "p_p_id": "phonebooksearch_WAR_phonebookportlet",
            "p_p_lifecycle": "2",
            "p_p_state": "normal",
            "p_p_mode": "view",
            "p_p_cacheability": "cacheLevelPage",
            "p_p_col_id": "column-2",
            "p_p_col_pos": "1",
            "p_p_col_count": "2",
            "_phonebooksearch_WAR_phonebookportlet_redirect": "",
            "_phonebooksearch_WAR_phonebookportlet_backURL": "",
            "_phonebooksearch_WAR_phonebookportlet_mode": "full-search",
            "_phonebooksearch_WAR_phonebookportlet_keyword": "",
            "_phonebooksearch_WAR_phonebookportlet_selectParent": "26010",
            "_phonebooksearch_WAR_phonebookportlet_pbName": "",
            "_phonebooksearch_WAR_phonebookportlet_pbFamily": "",
            "_phonebooksearch_WAR_phonebookportlet_pbEmail": "",
            "_phonebooksearch_WAR_phonebookportlet_pbDirNumber": "",
            "_phonebooksearch_WAR_phonebookportlet_pbIntNumber": "",
            "_phonebooksearch_WAR_phonebookportlet_pbMobileNumber": "",
            "_phonebooksearch_WAR_phonebookportlet_pbFax": "",
            "_phonebooksearch_WAR_phonebookportlet_pbOrganization": "26010",
            "_phonebooksearch_WAR_phonebookportlet_pbPost": "",
        }

    def get_employees(self):
        response = requests.post(
            self.url
            + "%D8%AA%D9%85%D8%A7%D8%B3-%D8%A8%D8%A7-%D8%AF%D8%A7%D9%86%D8%B4%DA%AF%D8%A7%D9%87?p_p_id=phonebooksearch_WAR_phonebookportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-2&p_p_col_pos=1&p_p_col_count=2",
            headers=self.headers,
            data=self.payload,
        )

        if response.status_code == 200:
            data = response.json()
            for item in data:
                if item.get("name"):
                    employee = Employee(
                        department=item.get("organizationname"),
                        name=item.get("name"),
                        role=item.get("organizationpost"),
                        internal_number=item.get("internalnumber"),
                        phone_number=item.get("mobile"),
                    )
                    return employee

    def get_colleges(self):
        pass

    def get_professors(self):
        pass

    def get_professor_page(self, professor, personal_page_link):
        pass

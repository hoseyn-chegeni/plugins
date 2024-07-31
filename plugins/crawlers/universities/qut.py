import requests
from bs4 import BeautifulSoup
from schemas.colleges import CollegeData 
from crawlers.universities.base import University
from crawlers.utils import check_connection
from schemas.professor import Professor


class QUTCrawler(University):

    def __init__(self) -> None:
        self.url = "https://www.qut.ac.ir/"


    def get_employees(self):
        pass

    def get_colleges(self):
        response = check_connection(requests.get, self.url + '/fa/wp/index' )
        soup = BeautifulSoup(response.text, "html.parser")
        th_elements = soup.find_all('th', attrs={'data-original-title': ''})
        
        # Iterate through each <th> element to check the text
        for th in th_elements:
            th_text = th.text.strip()
            if th_text.startswith("لیست اعضای هیئت علمی"):
                result_text = th_text[len("لیست اعضای هیئت علمی "):]
                college = CollegeData(value= result_text)
                return college

    def get_professors(self):
        response = check_connection(requests.get, self.url + '/fa/wp/index' )
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all('tr', attrs={'data-original-title': ''})
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 7:
                name = cells[1].text.strip()
                college = cells[2].text.strip()
                title = cells[3].text.strip()

                personal_page_link = cells[4].find('a', href=True)['href'].strip() if cells[4].find('a', href=True) else None
                google_scholar_link = cells[4].find_all('a', href=True)[1]['href'].strip() if len(cells[4].find_all('a', href=True)) > 1 else None
                scopus_link = cells[4].find_all('a', href=True)[2]['href'].strip() if len(cells[4].find_all('a', href=True)) > 2 else None

                email = cells[5].text.strip()
                image_src =  self.url + cells[6].find('img')['src'].strip() if cells[6].find('img') else None

                # If any element is None or empty, replace it with an empty list
                personal_page_link = self.url + personal_page_link if personal_page_link else None
                google_scholar_link = google_scholar_link if google_scholar_link else None
                scopus_link = scopus_link if scopus_link else None
                image_src = image_src if image_src else None
                
                professor = Professor(
                    full_name= name,
                    college= college,
                    rank= title,
                    email= email,
                    image= image_src
                
                )
                professor.socials.scholar = google_scholar_link
                professor.socials.scopus = scopus_link
                professor.socials.personal_cv = personal_page_link

                return professor


    def get_professor_page(self, link: str):
        pass

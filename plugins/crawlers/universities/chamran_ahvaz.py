import requests
from bs4 import BeautifulSoup
from crawlers.universities.base import University
from crawlers.utils import check_connection
from schemas.professor import Professor, Book
from schemas.employee import Employee
from urllib import parse
import re
from schemas.colleges import CollegeData

class ChamranAhvazCrawler(University):

    def __init__(self) -> None:
        self.url = "https://scu.ac.ir"

        self.emp_headers = {
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

        self.emp_payload = {
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


        self.prof_params = {
            'p_p_id': 'eduteacherdisplay_WAR_edumanagerportlet',
            'p_p_lifecycle': '0',
            'p_p_state': 'normal',
            'p_p_mode': 'view',
            'p_p_col_id': 'column-1',
            'p_p_col_count': '1',
            '_eduteacherdisplay_WAR_edumanagerportlet_mvcPath': '/edu-teacher-display/view.jsp',
            '_eduteacherdisplay_WAR_edumanagerportlet_delta': '75',
            '_eduteacherdisplay_WAR_edumanagerportlet_keywords': '',
            '_eduteacherdisplay_WAR_edumanagerportlet_advancedSearch': 'false',
            '_eduteacherdisplay_WAR_edumanagerportlet_andOperator': 'true',
            '_eduteacherdisplay_WAR_edumanagerportlet_lastName': '',
            '_eduteacherdisplay_WAR_edumanagerportlet_groupId': '0',
            '_eduteacherdisplay_WAR_edumanagerportlet_collegeSubGroupId': '0',
            '_eduteacherdisplay_WAR_edumanagerportlet_dependCollegeSubGroupId': '0',
            '_eduteacherdisplay_WAR_edumanagerportlet_resetCur': 'false',
            'cur': '1'
        }



    def get_employees(self):
        response = requests.post(
            self.url
            + "/%D8%AA%D9%85%D8%A7%D8%B3-%D8%A8%D8%A7-%D8%AF%D8%A7%D9%86%D8%B4%DA%AF%D8%A7%D9%87?p_p_id=phonebooksearch_WAR_phonebookportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-2&p_p_col_pos=1&p_p_col_count=2",
            headers=self.emp_headers,
            data=self.emp_payload,
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
                    #For test
                    print(employee)

                    #return employee

    def get_colleges(self):
        response = check_connection(requests.get,self.url + "/%D8%A7%D8%B9%D8%B6%D8%A7%DB%8C-%D9%87%DB%8C%DB%8C%D8%AA-%D8%B9%D9%84%D9%85%DB%8C")
        soup = BeautifulSoup(response.content, 'html.parser')
        select_element = soup.find('select', {'id': '_eduteacherdisplay_WAR_edumanagerportlet_groupId'})
        if select_element:
            options = select_element.find_all('option')
            for option in options:
                if option['value'] != '0':  
                    text = option.get_text(strip=True) 
                    college  = CollegeData(
                        value= text,
                        href= ''
                    )

                    #For test
                    print(college)

                    #return employee



    def get_professors(self):

        def get_page_url(base_url, params):
            return f"{base_url}?{parse.urlencode(params)}"
        
        while True:
            url = get_page_url(self.url +  "/اعضای-هییت-علمی" , self.prof_params)
           
            response = check_connection(requests.get, url)
            soup = BeautifulSoup(response.content, 'html.parser')
            h3_elements = soup.find_all('h3')

            links_found = False
            for h3 in h3_elements:
                link_tag = h3.find('a')
                if link_tag and 'href' in link_tag.attrs:
                    link = self.url+link_tag['href']
                    if link:
                        yield link
                    links_found = True

            if not links_found:
                break

            self.prof_params['cur'] = str(int(self.prof_params['cur']) + 1)


    def get_professor_page(self, link):
        response = check_connection(requests.get, link)
        soup = BeautifulSoup(response.content, 'html.parser')
        info_fields = soup.find_all('div', class_='info-field')
        name_tag = soup.find('h3')
        name = name_tag.get_text(strip=True)
        clean_name = re.sub(r'\(EN Page\)', '', name).strip()
        rank = info_fields[0].get_text(strip=True) if len(info_fields) > 0 else None
        college = info_fields[1].get_text(strip=True) if len(info_fields) > 1 else None
        email_img_tag = soup.select_one('div.info-field span.email img')
        email_img_src = email_img_tag['src'] if email_img_tag else None
        professor = Professor(
            full_name= clean_name,
            rank= rank,
            college= college
        )
        professor.email.append(email_img_src)
        # BOOKS
        try:
            book_texts = []
            divs = soup.find_all('div', id='_eduteacherdisplay_WAR_edumanagerportlet_tabs1971141161059910810111545971101004598111111107115TabsSection')
            for div in divs:
                # Find the <h3> tag with the specific text "کتب"
                h3_tag = div.find('h3', class_='cv-title', string="کتب")
                if h3_tag:
                    # If the <h3> tag is found, find all <a> tags with the class 'dsc-headlines'
                    a_tags = div.find_all('a', class_='dsc-headlines')
                    for a in a_tags:
                        book_texts.append(a.get_text(strip=True))
            combined_text = '\n\n'.join(book_texts)
            
            entries = combined_text.strip().split('\n\n')

            for entry in entries:
                parts = entry.split(',')
                authors = []
                title = None
                publisher = None
                publish_date = None
                place = None

                for part in parts:
                    part = part.strip()
                    if ': مترجم' in part or ': نویسنده' in part:
                        authors.append(part.split(':')[0].strip())
                    elif re.match(r'\d{4}', part):
                        publish_date = part
                    elif re.match(r'\d+-\d+-\d+', part):
                        publish_date = part
                    elif not title:
                        title = part
                    else:
                        if publisher is None:
                            publisher = part
                        elif place is None:
                            place = part

                professor.books.append(Book(
                    authors=authors,
                    title=title,
                    publish_date=publish_date,
                    place=place
                ))  
        except:
            pass
        
        # FOR TEST
        return professor


    def get_employee_page(self) -> Employee:
        return super().get_employee_page()
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
        professor_info = {}

        # Extract professor's name and title
        title_element = soup.select_one("span.news_titler")
        if title_element:
            professor_info['title'] = title_element.get_text(strip=True)
        
        # Extract image, email, phone numbers, and profile links
        contact_info_element = soup.select_one("p")
        if contact_info_element:
            # Extract the image source
            img_element = contact_info_element.find("img")
            if img_element:
                professor_info['image'] = img_element['src']
            
            # Extract the contact details
            spans = contact_info_element.find_all("span", recursive=False)
            if len(spans) > 0:
                contact_info = spans[0].get_text(separator="\n", strip=True)
                lines = contact_info.split("\n")
                
                for line in lines:
                    if "ایمیل:" in line:
                        professor_info['email'] = line.split(":", 1)[1].strip()
                    elif "تلفن مستقیم:" in line:
                        professor_info['phone_direct'] = line.split(":", 1)[1].strip()
                    elif "دورنگار:" in line:
                        professor_info['fax'] = line.split(":", 1)[1].strip()
                    elif "تلفن همراه" in line:
                        professor_info['phone_mobile'] = line.split(":", 1)[1].strip()

        profile_links = contact_info_element.find_all("a")
        for link in profile_links:
            href = link.get('href')
            if "researcher/1678952/vahid-safarifard" in href:
                professor_info['publons'] = href
            elif "scholar.google.com" in href:
                professor_info['google_scholar'] = href
            elif "scopus.com" in href:
                professor_info['scopus'] = href
            elif "orcid.org" in href:
                professor_info['orcid'] = href
            elif "researchgate.net" in href:
                professor_info['researchgate'] = href
            elif "mendeley.com" in href:
                professor_info['mendeley'] = href
            elif "persianmof.ir" in href:
                professor_info['research_group'] = href
            elif "chemistry.iust.ac.ir" in href:
                professor_info['homepage'] = href

        return professor_info
    

    # مهندسی شیمی نفت و گاز
    def get_professors_chemical_petroleum_and_gas_engineering(self):
        response = check_connection( requests.get, self.chemical_petroleum_and_gas_engineering + "/faculty/")
        soup = BeautifulSoup(response.content, "html.parser")
        h1_elements = soup.find_all("h1", style="text-align: right;")
        for h1 in h1_elements:
            a_tag = h1.find("a", href=True)
            if a_tag is not None:
                return f'{self.chemical_petroleum_and_gas_engineering}{a_tag['href']}'

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
        professor_info = {}
        # Extract information from the <td> element
        td_element = soup.find("td")
        if td_element:
            # Extract the professor's name
            name_element = td_element.find("font", size="2")
            if name_element:
                professor_info['name'] = name_element.get_text(strip=True).strip('"')
            # Extract title, group, email, and phone
            strong_elements = td_element.find_all("strong")
            for element in strong_elements:
                text = element.get_text(strip=True)
                if "استاد" in text and "عضو" not in text:
                    professor_info['title'] = text
                elif "عضو گروه" in text:
                    professor_info['group'] = text
                elif "Email" in text:
                    professor_info['email'] = text.split(":", 1)[1].strip().replace("AT", "@")
                elif "تلفن" in text:
                    professor_info['phone'] = text.split(":", 1)[1].strip()
        return professor_info


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
        
        # Extracting data from the first div element
        profile_div = soup.find("div", {"id": "sidebar-title"})
        if not profile_div:
            return None
        
        profile_img_tag = profile_div.find("img", {"class": "img-fluid"})
        profile_img_url = profile_img_tag["src"] if profile_img_tag else None
        
        alt_img_tag = profile_div.find("img", {"src": "./files/fnst/images/Faculty_Member/Dr.Rahmani.png"})
        alt_img_url = alt_img_tag["src"] if alt_img_tag else None
        
        professor_name_tag = profile_div.find("h3")
        professor_name = professor_name_tag.text.strip() if professor_name_tag else None
        
        professor_title_tag = profile_div.find("p")
        professor_title = professor_title_tag.text.strip() if professor_title_tag else None
        
        # Extracting data from the second div element
        contact_div = soup.find("div", {"class": "section px-3"})
        if not contact_div:
            return None
        
        contact_info = {}
        contact_list_items = contact_div.find_all("li", {"class": "d-flex align-items-center"})
        
        for item in contact_list_items:
            contact_icon = item.find("span", {"class": "contact-icon"}).find("i")
            contact_value = item.find("strong")
            if contact_icon and contact_value:
                icon_class = contact_icon["class"][1]  # assuming the second class is the specific icon type
                contact_info[icon_class] = contact_value.text.strip()
        
        return {
            "profile_img_url": profile_img_url,
            "alt_img_url": alt_img_url,
            "professor_name": professor_name,
            "professor_title": professor_title,
            "contact_info": contact_info
        }


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
            if not response:
                return None
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            data = {}
            
            # Extract the professor's name
            name_element = soup.find("h2", class_="elementor-heading-title elementor-size-large")
            data['name'] = name_element.text.strip() if name_element else "N/A"
            
            # Extract academic rank
            academic_rank_element = None
            contact_elements = soup.find_all("li", class_="elementor-icon-list-item")
            for element in contact_elements:
                if "مرتبه علمی" in element.get_text(strip=True):
                    academic_rank_element = element
                    break
            
            data['academic_rank'] = academic_rank_element.get_text(strip=True) if academic_rank_element else "N/A"
            
            # Extract contact information
            contact_info = {}
            for element in contact_elements:
                text = element.get_text(strip=True)
                if "تلفن" in text:
                    contact_info['phone'] = text
                elif "فاکس" in text:
                    contact_info['fax'] = text
                elif "ایمیل" in text:
                    contact_info['email'] = text
                elif "آدرس" in text:
                    contact_info['address'] = text
            
            data['contact_info'] = contact_info
            
            # Extract external links
            external_links = {}
            external_link_elements = soup.find_all("a", class_="elementor-icon-list-item-link")
            
            for element in external_link_elements:
                link_text = element.get_text(strip=True)
                href = element.get('href')
                external_links[link_text] = href
            
            data['external_links'] = external_links
            
            return data



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

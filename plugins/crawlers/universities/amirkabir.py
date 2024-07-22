import requests
from bs4 import BeautifulSoup

from crawlers.universities.base import University
from crawlers.utils import check_connection
from schemas import (
    Activity,
    Book,
    Course,
    EducationalRecord,
    Employee,
    Honor,
    Interest,
    Invention,
    Membership,
    Language,
    Professor,
    Skill,
    Thesis,
    Workshop,
)


class AmirkabirCrawler(University):
    def __init__(self) -> None:
        self.url = "https://aut.ac.ir/"

    def get_employees(self):
        response = check_connection(
            requests.get, self.url + "persons.php?slc_lang=fa&sid=1&list_sections=1/fa/"
        )
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.find_all(
            "a", attrs={"style": "font-family:yekanYW; font-size:15px !important;"}
        ):
            yield self.url + link["href"]

    def get_professors(self):
        response = check_connection(
            requests.get, self.url + "cv.php?slc_lang=fa&sid=1&show_all=1"
        )
        soup = BeautifulSoup(response.text, "html.parser")
        for row in soup.find("div", {"class": "table"}).find_all(
            "div", {"class": "row"}
        )[1:]:
            yield self.url + row.find("a")["href"][2:]

    def get_professor_page(self, link: str):
        response = check_connection(requests.get, link)
        soup = BeautifulSoup(response.text, "html.parser")
        cv_level = []
        for br in soup.find("div", {"class": "cv_level"}).find_all("br"):
            cv_level.append(br.previous_sibling)
        cv_level.append(br.next_sibling)

        professor = Professor(
            college=cv_level[1],
            full_name=soup.find("div", {"class": "name"}).text.strip(),
            group=cv_level[2],
            image=self.url
            + soup.find("img", {"class": "yekta_thumb cv_photo"})["src"][2:],
            rank=cv_level[0],
            university_link=link,
        )

        for item in soup.find("div", {"class": "list_title"}).find_all(
            "div", {"class": "items"}
        ):
            # Find the 'title' and 'value' divs within the current 'item'
            title_div = item.find("div", {"class": "title"})
            value_div = item.find("div", {"class": "value"})
            if "پست الکترونیک" in title_div.text:
                professor.email = value_div.text.strip()
            elif "شماره تماس" in title_div.text:
                professor.phone_number = value_div.text.strip()
            elif "h-index" in title_div.text:
                professor.h_index = value_div.text.strip()
            elif "ارجاعات" in title_div.text:
                professor.references = value_div.text.strip()

        # Socials
        social_soup = soup.find("div", {"class": "social"})
        if social_soup:
            try:
                professor.socials.orcid(
                    social_soup.find("a", {"class": "orcid masterTooltip "})["href"]
                )
            except:
                pass
            try:
                professor.socials.scopus(
                    social_soup.find("a", {"class": "scopus masterTooltip "})["href"]
                )
            except:
                pass
            try:
                professor.socials.twitter(
                    social_soup.find("a", {"class": "twitter masterTooltip "})["href"]
                )
            except:
                pass
            try:
                professor.socials.google(
                    social_soup.find("a", {"class": "google masterTooltip "})["href"]
                )
            except:
                pass
            try:
                professor.socials.telegram(
                    social_soup.find("a", {"class": "telegram masterTooltip "})["href"]
                )
            except:
                pass
            try:
                professor.socials.researchgate(
                    social_soup.find("a", {"class": "researchgate masterTooltip "})[
                        "href"
                    ]
                )
            except:
                pass
            try:
                professor.socials.scholar(
                    social_soup.find("a", {"class": "scholar masterTooltip "})["href"]
                )
            except:
                pass

        # Doctoral thesis
        doctoral_soup = soup.find("div", {"id": "cv_link_31"})
        if doctoral_soup:
            for row in doctoral_soup.find_all("div", {"class": "row"})[1:]:
                details = [
                    cell.text.strip() for cell in row.find_all("div", {"class": "cell"})
                ]
                professor.doctoral_thesis.append(
                    Thesis(
                        authors=[author for author in details[2].split(" و ")],
                        defense_date=details[3],
                        title=details[1],
                    )
                )

        # Masters thesis
        masters_soup = soup.find("div", {"id": "cv_link_32"})
        if masters_soup:
            for row in masters_soup.find_all("div", {"class": "row"})[1:]:
                details = [
                    cell.text.strip() for cell in row.find_all("div", {"class": "cell"})
                ]
                professor.masters_thesis.append(
                    Thesis(
                        authors=[author for author in details[2].split(" و ")],
                        defense_date=details[3],
                        title=details[1],
                    )
                )

        # Journal articles
        journal_soup = soup.find("div", {"id": "cv_link_14"})
        if journal_soup:
            for row in journal_soup.find_all("div", {"class": "row ltr"}):
                professor.journal_articles.append(row.text.strip())

        # Conference papers
        conference_soup = soup.find("div", {"id": "cv_link_16"})
        if conference_soup:
            for row in conference_soup.find_all("div", {"class": "row ltr"}):
                professor.conference_papers.append(row.text.strip())

        # Courses
        courses_soup = soup.find("div", {"id": "cv_link_28"})
        if courses_soup:
            for row in courses_soup.find_all("div", {"class": "row"})[1:]:
                details = [
                    cell.text.strip() for cell in row.find_all("div", {"class": "cell"})
                ]
                professor.courses.append(
                    Course(description=details[2], period=details[4], title=details[1])
                )

        # Inventions
        invention_soup = soup.find("div", {"id": "cv_link_29"})
        if invention_soup:
            for row in invention_soup.find_all("div", {"class": "row"})[2:]:
                details = [
                    cell.text.strip() for cell in row.find_all("div", {"class": "cell"})
                ]
                professor.inventions.append(
                    Invention(
                        country=details[3],
                        expiration_date=details[6],
                        partners=[partner for partner in details[4].split(",")],
                        registration_date=details[5],
                        registration_number=details[2],
                        title=details[1],
                    )
                )

        # Books
        book_soup = soup.find("div", {"id": "cv_link_13"})
        if book_soup:
            for row in book_soup.find_all("div", {"class": "row"})[2:]:
                details = [
                    cell.text.strip() for cell in row.find_all("div", {"class": "cell"})
                ]
                professor.books.append(
                    Book(
                        authors=[partner for partner in details[2].split(",")],
                        copy_num=details[5],
                        place=details[3],
                        publish_date=details[4],
                        title=details[1],
                    )
                )

        # Language
        language_soup = soup.find("div", {"id": "cv_link_3"})
        if language_soup:
            for row in language_soup.find_all("div", {"class": "row"})[1:]:
                details = [
                    cell.text.strip() for cell in row.find_all("div", {"class": "cell"})
                ]
                professor.languages.append(
                    Language(
                        language=details[1], speaking=details[3], translate=details[2]
                    )
                )

        # Educational records
        educational_soup = soup.find("div", {"id": "cv_link_2"})
        if educational_soup:
            for row in educational_soup.find_all("div", {"class": "row"})[1:]:
                details = [
                    cell.text.strip() for cell in row.find_all("div", {"class": "cell"})
                ]
                try:
                    degree, study_field = details[1].split("/")
                except:
                    degree = study_field = details[1]
                professor.educational_records.append(
                    EducationalRecord(
                        city=details[3],
                        country=details[4],
                        degree=degree,
                        graduation_date=details[5],
                        study_field=study_field,
                        university=details[2],
                    )
                )

        # Research interests
        interests_soup = soup.find("div", {"id": "cv_link_6"})
        if interests_soup:
            for row in interests_soup.find_all("div", {"class": "row"})[1:]:
                details = [
                    cell.text.strip() for cell in row.find_all("div", {"class": "cell"})
                ]
                professor.interests.append(
                    Interest(start_date=details[2], title=details[1])
                )

        # Operating activities
        activities_soup = soup.find("div", {"id": "cv_link_25"})
        if activities_soup:
            for row in activities_soup.find_all("div", {"class": "row"})[1:]:
                details = [
                    cell.text.strip() for cell in row.find_all("div", {"class": "cell"})
                ]
                try:
                    location, description = details[2].split("/")
                except:
                    location = description = details[2]
                professor.activities.append(
                    Activity(
                        description=description,
                        end_date=details[4],
                        location=location,
                        start_date=details[3],
                        title=details[1],
                    )
                )

        # Professional skills
        skills_soup = soup.find("div", {"id": "cv_link_4"})
        if skills_soup:
            for row in skills_soup.find_all("div", {"class": "row"})[1:]:
                details = [
                    cell.text.strip() for cell in row.find_all("div", {"class": "cell"})
                ]
                professor.skills.append(Skill(title=details[1], start_date=details[2]))

        # Magazines membership
        membership_soup = soup.find("div", {"id": "cv_link_17"})
        if membership_soup:
            for row in membership_soup.find_all("div", {"class": "row"})[1:]:
                details = [
                    cell.text.strip() for cell in row.find_all("div", {"class": "cell"})
                ]
                professor.magazines_membership.append(
                    Membership(title=details[1], description=details[2])
                )

        # Professional membership
        professional_soup = soup.find("div", {"id": "cv_link_21"})
        if professional_soup:
            for row in professional_soup.find_all("div", {"class": "row"})[1:]:
                details = [
                    cell.text.strip() for cell in row.find_all("div", {"class": "cell"})
                ]
                professor.professional_membership.append(
                    Membership(title=details[1], description=details[2])
                )

        # Honors and awards
        honors_soup = soup.find("div", {"id": "cv_link_20"})
        if honors_soup:
            for row in honors_soup.find_all("div", {"class": "row"})[1:]:
                details = [
                    cell.text.strip() for cell in row.find_all("div", {"class": "cell"})
                ]
                professor.honors.append(Honor(title=details[1], date=details[2]))

        # Workshops
        workshops_soup = soup.find("div", {"id": "cv_link_8"})
        if workshops_soup:
            for row in workshops_soup.find_all("div", {"class": "row"})[1:]:
                details = [
                    cell.text.strip() for cell in row.find_all("div", {"class": "cell"})
                ]
                professor.workshops.append(
                    Workshop(
                        title=details[1],
                        organizing=details[2],
                        event_place=details[3],
                        event_date=details[4],
                    )
                )

        return professor

    def get_employee_page(self):
        response = check_connection(
            requests.get, self.url + "persons.php?sid=1&slc_lang=fa#person_part"
        )
        soup = BeautifulSoup(response.text, "html.parser")

        soup = soup.find("div", {"id": "default_data"}).find(
            "div", {"style": "clear:both;"}
        )
        department = None
        while True:
            soup = soup.find_next_sibling()
            if not soup:
                break
            if soup.name == "div":
                a = soup.find(
                    "a", {"style": "font-family:yekanYW; font-size:15px !important;"}
                )
                if a:
                    department = a.text.strip()
            elif soup.name == "a":
                details_soup = soup.find(
                    "div",
                    {
                        "class": "yw_prsn_box yw_gradient_black1 yw_linh_normal yw_radius yw_hover yw_black_txt yw_width_350 yw_margin_10 pad5 f12 yw_table_col_1"
                    },
                )
                img = self.url + details_soup.find("img")["src"][2:]

                d = details_soup.find("div", {"align": "justify"})
                nums = d.find_all("span", {"dir": "ltr"})

                yield Employee(
                    department=department,
                    image=img,
                    name=d.find("strong").text.strip(),
                    role=d.text.split("\n")[3].strip(),
                    internal_number=nums[0].text.strip(),
                    phone_number=nums[1].text.strip(),
                )


amirkabir_crawler = AmirkabirCrawler()

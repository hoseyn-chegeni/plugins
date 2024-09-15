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
import re


class TehranQarbCrawler(University):
    def __init__(self) -> None:
        self.url = ""

    def get_employees(self):
        pass

    def get_colleges(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto("https://wtb.iau.ir/fa")
            page.wait_for_selector("ul")
            page_content = page.content()
            browser.close()

        soup = BeautifulSoup(page_content, "html.parser")
        ul_elements = soup.find_all("ul", class_="dropdown-menu")
        pattern = re.compile(r"دانشکده")
        for ul in ul_elements:
            faculties = ul.find_all("h4")

            for faculty in faculties:
                a_tag = faculty.find("a")
                if a_tag and pattern.search(a_tag.text):
                    faculty_name = a_tag.text.strip()
                    faculty_url = "https://wtb.iau.ir" + a_tag["href"]
                    college = CollegeData(href=faculty_url, value=faculty_name)
                    yield college

    def get_professors(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for page_number in range(1, 19):
                url = f"https://wtb.iau.ir/faculty/fa?%2Ffa=&page={page_number}&per-page=18"
                page.goto(url)
                page.wait_for_selector("form")
                content = page.content()
                soup = BeautifulSoup(content, "html.parser")
                faculty_items = soup.find_all(
                    "div", class_="item grid-group-item col-sm-6 col-lg-4"
                )

                for item in faculty_items:
                    list_caption = item.find("div", class_="list-caption")
                    if list_caption:
                        link_tag = list_caption.find("a", href=True)
                        link = link_tag["href"]
                        yield link
            browser.close()

    def get_professor_page(self, link) -> Professor:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(link)
            page.wait_for_selector("div.panel-body")
            content = page.content()
            browser.close()

        soup = BeautifulSoup(content, "html.parser")
        profile_div = soup.find("div", class_="col-xs-12 profile-sidebar")
        if profile_div:
            img_div = profile_div.find("div", class_="profile-userpic")
            if img_div and img_div.find("img"):
                img_url = img_div.find("img")["src"]

            name_div = profile_div.find("div", class_="profile-usertitle-name")
            job_title_div = profile_div.find("div", class_="profile-usertitle-job")
            if name_div:
                name = name_div.get_text(strip=True)
            if job_title_div:
                job_title = job_title_div.get_text(strip=True)

            scholar_link_div = profile_div.find("a", class_="btn btn-teal")
            if scholar_link_div:
                scholar_link = scholar_link_div["href"]

            professor = Professor(full_name=name, rank=job_title, image=img_url)
            professor.socials.scholar = scholar_link

        # سوابق اموزشی
        try:
            education_div = soup.find("div", id="educations-data")
            if education_div:
                table = education_div.find(
                    "table", class_="table table-striped table-bordered"
                )
                headers = [th.text.strip() for th in table.find_all("th")]
                rows = table.find("tbody").find_all("tr")
                for row in rows:
                    cols = row.find_all("td")
                    academic_rank = cols[0].text.strip()
                    year = cols[1].text.strip() if cols[1].text.strip() else "N/A"
                    major = cols[2].text.strip()
                    university = cols[3].text.strip()
                    professor.educational_records.append(
                        EducationalRecord(
                            degree=academic_rank,
                            graduation_date=year,
                            university=university,
                            study_field=major,
                        )
                    )
        except:
            pass

        # سوابق استخدام
        try:
            employment_div = soup.find("div", id="employment-data")
            if employment_div:
                table = employment_div.find(
                    "table", class_="table table-striped table-bordered"
                )
                rows = table.find("tbody").find_all("tr")
                for row in rows:
                    cols = row.find_all("td")
                    place_of_service = cols[0].text.strip()
                    position = cols[1].text.strip()
                    employment_type = cols[2].text.strip()
                    cooperation_type = cols[3].text.strip()
                    professor.job_experiences.append(
                        JobExperience(
                            title=f"محل خدمت: {place_of_service}, عنوان سمت: {position}, نوع استخدام: {employment_type}, نوع همکاری: {cooperation_type}"
                        )
                    )
        except:
            pass

        # سوابق اجرایی
        try:
            tabs = {
                "menu0": "سوابق اجرایی",
                "menu1": "جوایز و تقدیر نامه ها",
                "menu2": "موضوعات تدریس تخصصی",
                "menu3": "فعالیت های علمی و اجرایی",
                "menu4": "زمینه های تدریس",
            }

            for menu_id in tabs.items():
                tab_content = soup.find("div", id=menu_id)
                if tab_content:
                    text_content = tab_content.get_text(separator="\n").strip()
                    if menu_id == "menu0":
                        activity_entries = text_content.split("\n\n")

                        for entry in activity_entries:
                            activity = Activity(
                                title=entry,
                            )

                            professor.activities.append(activity)
        except:
            pass

        # سوابق علمی و اجرایی
        try:
            tabs = {
                "menu0": "سوابق اجرایی",
                "menu1": "جوایز و تقدیر نامه ها",
                "menu2": "موضوعات تدریس تخصصی",
                "menu3": "فعالیت های علمی و اجرایی",
                "menu4": "زمینه های تدریس",
            }

            for menu_id, tab_name in tabs.items():
                tab_content = soup.find("div", id=menu_id)
                if tab_content:
                    text_content = tab_content.get_text(separator="\n").strip()
                    if menu_id == "menu3":
                        activity_entries = text_content.split("\n\n")

                        for entry in activity_entries:
                            activity = Activity(
                                title=entry,
                            )

                            professor.activities.append(activity)
        except:
            pass

        #  افتخارات
        try:
            tabs = {
                "menu0": "سوابق اجرایی",
                "menu1": "جوایز و تقدیر نامه ها",
                "menu2": "موضوعات تدریس تخصصی",
                "menu3": "فعالیت های علمی و اجرایی",
                "menu4": "زمینه های تدریس",
            }

            for menu_id, tab_name in tabs.items():
                tab_content = soup.find("div", id=menu_id)
                if tab_content:
                    text_content = tab_content.get_text(separator="\n").strip()
                    if menu_id == "menu1":
                        honor_entries = text_content.split("\n\n")

                        for entry in honor_entries:
                            honor = Honor(
                                title=entry,
                            )
                            professor.honors.append(honor)
        except:
            pass

        return professor

    def get_employee_page(self) -> Employee:
        return super().get_employee_page()

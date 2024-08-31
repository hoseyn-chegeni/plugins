from bs4 import BeautifulSoup
from crawlers.universities.base import University
from schemas.employee import Employee
from playwright.sync_api import sync_playwright
from schemas.colleges import CollegeData
from schemas.professor import Professor
from crawlers.universities.azad.groups import (
    # اقتصاد
    get_eghtesad__hesabdari_prof,
    get_eghtesad__nazari_sanati_prof,
    get_eghtesad__bazargani_prof,
    # علوم انسانی
    get_ensani__adian_erfan_prof,
    get_ensani__falsafe_gharb_prof,
    get_ensani__feghh_hoghugh_prof,
    get_ensani__qoran_hadis_prof,
    get_ensani__tarikh_prof,
    get_ensani__zaban_arab_prof,
    get_ensnai__joghrafi_prof,
    get_ensnai__zaban_farsi_prof,
    get_ensnai__falsafe_prof,
    # تربیت بدنی
    get_tarbiat_badani__olum_varzeshi_prof,
    get_tarbiat_badani__raftar_harkati_prof,
    get_tarbiat_badani__physiology_varzeshi_prof,
    get_tarbiat_badani__biomechanic_prof,
    #  هنر
    get_honar__namayesh_prof,
    get_honar__music_prof,
    get_honar__naghashi_prof,
    get_honar__akasi_prof,
    get_honar__tarahi_sanati_prof,
    get_honar__pazhouhesh_honar_prof,
    #حقوق
    get_hoghugh_prof,
    # علوم اجتماعی
    get_olum_ejtemaee__farhang_resane_prof,   
    get_olum_ejtemaee__ertebatat_prof, 
    get_olum_ejtemaee__prof,
    get_olum_ejtemaee__jame_shenasi_prof,
    get_olum_ejtemaee__mardom_shenasi_prof,
)


class TehranMarkazCrawler(University):
    def __init__(self) -> None:
        self.url = "https://ctb.iau.ir"

    def get_employees(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            base_url = "https://ctb.iau.ir/fa/grid/16/%D8%A7%D8%B7%D9%84%D8%A7%D8%B9%D8%A7%D8%AA-%D8%AA%D9%85%D8%A7%D8%B3?GridSearch%5BpageSize%5D=200&GridSearch%5Bsearch%5D=&page="
            page_num = 1
            previous_first_row = None

            while True:
                url = f"{base_url}{page_num}&per-page=200"
                page.goto(url)
                page.wait_for_selector("td")
                page_content = page.content()
                soup = BeautifulSoup(page_content, "html.parser")
                tr_elements = soup.find_all("tr")
                all_rows = []
                for tr in tr_elements:
                    td_elements = tr.find_all("td")
                    row = [td.get_text(strip=True) for td in td_elements]
                    if row and not row[0] == "":
                        all_rows.append(row)
                if all_rows:
                    current_first_row = all_rows[0]
                    if previous_first_row and current_first_row == previous_first_row:
                        break
                    for row in all_rows:
                        employee = Employee(
                            name=row[1],
                            role=row[2],
                            department=row[3],
                            internal_number=row[4],
                            phone_number=row[5],
                        )
                        yield employee
                    previous_first_row = current_first_row
                else:
                    break
                page_num += 1
            browser.close()

    def get_colleges(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://ctb.iau.ir/fa")
            page.wait_for_selector("ul#wb08a2d9f4c3791de4252d29fb27982a15")
            page_content = page.content()
            browser.close()
            soup = BeautifulSoup(page_content, "html.parser")
            ul_element = soup.find("ul", id="wb08a2d9f4c3791de4252d29fb27982a15")
            links = ul_element.find_all("a")
            for link in links[1:]:
                href = link.get("href")
                if not href.startswith("http"):
                    href = "https://ctb.iau.ir" + href
                college = CollegeData(href=href, value=link.text.strip())
                yield college

    def get_professors(self):
        # # ادبیات علوم انسانی -علوم قرآن و حدیث
        # for professor in get_ensani__qoran_hadis_prof():
        #     yield professor

        # # ادبیات علوم انسانی -   ادیان و عرفان اسلامی
        # for professor in get_ensani__adian_erfan_prof():
        #     yield professor

        # # ادبیات علوم انسانی -   فقه و حقوق اسلامی
        # for professor in get_ensani__feghh_hoghugh_prof():
        #     yield professor

        # # ادبیات علوم انسانی -  تاریخ و باستانشناسی
        # for professor in get_ensani__tarikh_prof():
        #     yield professor

        # # ادبیات علوم انسانی - فلسفه و حکمت اسلامی
        # for professor in get_ensnai__falsafe_prof():
        #     yield professor

        # # ادبیات علوم انسانی - فلسفه غرب
        # for professor in get_ensani__falsafe_gharb_prof():
        #     yield professor

        # # ادبیات علوم انسانی -  جغرافیا
        # for professor in get_ensnai__joghrafi_prof():
        #     yield professor

        # # ادبیات علوم انسانی -  زبان و ادبیات فارسی
        # for professor in get_ensnai__zaban_farsi_prof():
        #     yield professor

        # # ادبیات علوم انسانی - زبان و ادبیات عرب
        # for professor in get_ensani__zaban_arab_prof():
        #     yield professor

        # # اقتصاد و حسابداری - گروه حسابداری
        # for professor in get_eghtesad__hesabdari_prof():
        #     yield professor

        # # اقتصاد و حسابداری - گروه اقتصاد بازرگانی و حمل ونقل
        # for professor in get_eghtesad__bazargani_prof():
        #     yield professor

        # # اقتصاد و حسابداری - گروه اقتصاد نظری و صنعتی
        # for professor in get_eghtesad__nazari_sanati_prof():
        #     yield professor

        # # تربیت بدنی - علوم ورزشی
        # for professor in get_tarbiat_badani__olum_varzeshi_prof():
        #     yield professor

        # # تربیت بدنی -  رفتار حرکتی
        # for professor in get_tarbiat_badani__raftar_harkati_prof():
        #     yield professor

        # # تربیت بدنی -  فیزیولوژی ورزشی
        # for professor in get_tarbiat_badani__physiology_varzeshi_prof():
        #     yield professor

        # # تربیت بدنی -  فیزیولوژی ورزشی
        # for professor in get_tarbiat_badani__biomechanic_prof():
        #     yield professor

        # # هنر  -   نمایش
        # for professor in get_honar__namayesh_prof():
        #     yield professor

        # # هنر  -   موسیقی
        # for professor in get_honar__music_prof():
        #     yield professor

        # # هنر  -   نقاشی
        # for professor in get_honar__naghashi_prof():
        #     yield professor

        # # هنر  -   عکاسی
        # for professor in get_honar__akasi_prof():
        #     yield professor

        # # هنر  -   طراحی صنعتی
        # for professor in get_honar__tarahi_sanati_prof():
        #     yield professor

        # # هنر  -    پژوهش هنر
        # for professor in get_honar__pazhouhesh_honar_prof():
        #     yield professor

        # #  حقوق
        # for professor in get_hoghugh_prof():
        #     yield professor

        # #دانشکده علوم اجتماعی - فرهنگ و رسانه
        # for professor in get_olum_ejtemaee__farhang_resane_prof():
        #     yield professor

        # #دانشکده علوم اجتماعی -   ارتباطات، روزنامه نگاری و رسانه
        # for professor in get_olum_ejtemaee__ertebatat_prof():
        #     yield professor

        # #دانشکده علوم اجتماعی -  گروه علوم اجتماعی
        # for professor in get_olum_ejtemaee__prof():
        #     yield professor

        # #دانشکده علوم اجتماعی - جامعه شناسی  
        # for professor in get_olum_ejtemaee__jame_shenasi_prof():
        #     yield professor


        #دانشکده علوم اجتماعی - مردم شناسی  
        for professor in get_olum_ejtemaee__mardom_shenasi_prof():
            yield professor

    def get_professor_page(self) -> Professor:
        return super().get_professor_page()

    def get_employee_page(self) -> Employee:
        return super().get_employee_page()

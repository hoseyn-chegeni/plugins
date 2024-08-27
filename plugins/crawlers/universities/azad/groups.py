from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from schemas.professor import Professor, EducationalRecord


# ادبیات علوم انسانی -علوم قرآن و حدیث
def get_ensani__qoran_hadis_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://ctb.iau.ir/literature/fa/page/1924/%D8%B9%D9%84%D9%88%D9%85-%D9%82%D8%B1%D8%A2%D9%86-%D9%88-%D8%AD%D8%AF%DB%8C%D8%AB"
        )
        page.wait_for_selector("table")  # Adjust this selector if needed
        content = page.content()
        browser.close()
    soup = BeautifulSoup(content, "html.parser")
    table = soup.find("table")
    if table is None:
        return
    try:
        for row in table.find("tbody").find_all("tr"):
            cells = row.find_all("td")
            professor = Professor(
                full_name=cells[1].text.strip(),
                rank=cells[3].text.strip(),
                group="علوم قرآن و حدیث",
                educational_records=[EducationalRecord(title=cells[4].text.strip())],
                college="ادبیات و علوم انسانی ",
            )
            yield professor
    except:
        pass


# ادبیات علوم انسانی -   ادیان و عرفان اسلامی
def get_ensani__adian_erfan_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://ctb.iau.ir/literature/fa/page/1924/%D8%B9%D9%84%D9%88%D9%85-%D9%82%D8%B1%D8%A2%D9%86-%D9%88-%D8%AD%D8%AF%DB%8C%D8%AB"
        )
        page.wait_for_selector("table")  # Adjust this selector if needed
        content = page.content()
        browser.close()
    soup = BeautifulSoup(content, "html.parser")
    table = soup.find("table")
    if table is None:
        return
    try:
        for row in table.find("tbody").find_all("tr"):
            cells = row.find_all("td")
            professor = Professor(
                full_name=cells[1].text.strip(),
                rank=cells[3].text.strip(),
                group="ادیان و عرفان اسلامی",
                educational_records=[EducationalRecord(title=cells[4].text.strip())],
                college="ادبیات و علوم انسانی ",
            )
            yield professor
    except:
        pass


# ادبیات علوم انسانی -   فقه و حقوق اسلامی
def get_ensani__feghh_hoghugh_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://ctb.iau.ir/literature/fa/page/1923/%D9%81%D9%82%D9%87-%D9%88-%D8%AD%D9%82%D9%88%D9%82-%D8%A7%D8%B3%D9%84%D8%A7%D9%85%DB%8C"
        )
        page.wait_for_selector("table")  # Adjust this selector if needed
        content = page.content()
        browser.close()
    soup = BeautifulSoup(content, "html.parser")
    table = soup.find("table")
    if table is None:
        return
    try:
        for row in table.find("tbody").find_all("tr"):
            cells = row.find_all("td")
            professor = Professor(
                full_name=cells[1].text.strip(),
                rank=cells[3].text.strip(),
                group="فقه و حقوق اسلامی",
                educational_records=[EducationalRecord(title=cells[4].text.strip())],
                college="ادبیات و علوم انسانی ",
            )
            yield professor
    except:
        pass


# ادبیات علوم انسانی -  تاریخ و باستانشناسی
def get_ensani__tarikh_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://ctb.iau.ir/literature/fa/page/1922/%D8%AA%D8%A7%D8%B1%DB%8C%D8%AE-%D9%88-%D8%A8%D8%A7%D8%B3%D8%AA%D8%A7%D9%86%D8%B4%D9%86%D8%A7%D8%B3%DB%8C"
        )
        page.wait_for_selector("table")  # Adjust this selector if needed
        content = page.content()
        browser.close()
    soup = BeautifulSoup(content, "html.parser")
    table = soup.find("table")
    if table is None:
        return
    try:
        for row in table.find("tbody").find_all("tr"):
            cells = row.find_all("td")
            professor = Professor(
                full_name=cells[1].text.strip(),
                rank=cells[3].text.strip(),
                group="تاریخ و باستانشناسی",
                educational_records=[EducationalRecord(title=cells[4].text.strip())],
                college="ادبیات و علوم انسانی ",
            )
            yield professor
    except:
        pass


# ادبیات علوم انسانی -  فلسفه و حکمت اسلامی
def get_ensnai__falsafe_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://ctb.iau.ir/literature/fa/page/1921/%D9%81%D9%84%D8%B3%D9%81%D9%87-%D9%88-%D8%AD%DA%A9%D9%85%D8%AA-%D8%A7%D8%B3%D9%84%D8%A7%D9%85%DB%8C"
        )
        page.wait_for_selector("table")  # Adjust this selector if needed
        content = page.content()
        browser.close()
    soup = BeautifulSoup(content, "html.parser")
    table = soup.find("table")
    if table is None:
        return
    try:
        for row in table.find("tbody").find_all("tr"):
            cells = row.find_all("td")
            professor = Professor(
                full_name=cells[1].text.strip(),
                rank=cells[3].text.strip(),
                group="فلسفه و حکمت اسلامی",
                educational_records=[EducationalRecord(title=cells[4].text.strip())],
                college="ادبیات و علوم انسانی ",
            )
            yield professor
    except:
        pass


# ادبیات علوم انسانی - فلسفه غرب
def get_ensani__falsafe_gharb_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://ctb.iau.ir/literature/fa/page/1920/%D9%81%D9%84%D8%B3%D9%81%D9%87-%D8%BA%D8%B1%D8%A8"
        )
        page.wait_for_selector("table")
        content = page.content()
        browser.close()
    soup = BeautifulSoup(content, "html.parser")
    table = soup.find("table")
    if table is None:
        return
    try:
        for row in table.find("tbody").find_all("tr"):
            cells = row.find_all("td")
            professor = Professor(
                full_name=cells[1].text.strip(),
                rank=cells[3].text.strip(),
                group="فلسفه غرب",
                educational_records=[EducationalRecord(title=cells[4].text.strip())],
                college="ادبیات و علوم انسانی ",
            )
            yield professor
    except:
        pass


# ادبیات علوم انسانی -  جغرافیا


def get_ensnai__joghrafi_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://ctb.iau.ir/literature/fa/page/1919/%D8%AC%D8%BA%D8%B1%D8%A7%D9%81%DB%8C%D8%A7"
        )
        page.wait_for_selector("table")
        content = page.content()
        browser.close()
    soup = BeautifulSoup(content, "html.parser")
    table = soup.find("table")
    if table is None:
        return
    try:
        for row in table.find("tbody").find_all("tr"):
            cells = row.find_all("td")
            professor = Professor(
                full_name=cells[1].text.strip(),
                rank=cells[3].text.strip(),
                group="جغرافیا",
                educational_records=[EducationalRecord(title=cells[4].text.strip())],
                college="ادبیات و علوم انسانی ",
            )
            yield professor
    except:
        pass


# ادبیات علوم انسانی -  زبان و ادبیات فارسی
def get_ensnai__zaban_farsi_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://ctb.iau.ir/literature/fa/page/1917/%D8%B2%D8%A8%D8%A7%D9%86-%D9%88-%D8%A7%D8%AF%D8%A8%DB%8C%D8%A7%D8%AA-%D9%81%D8%A7%D8%B1%D8%B3%DB%8C"
        )
        page.wait_for_selector("table")
        content = page.content()
        browser.close()

    soup = BeautifulSoup(content, "html.parser")
    tables = soup.find_all("table")  # Find all tables on the page

    if not tables:
        return

    try:
        for table in tables:
            for row in table.find("tbody").find_all("tr"):
                cells = row.find_all("td")
                professor = Professor(
                    full_name=cells[1].text.strip(),
                    rank=cells[3].text.strip(),
                    group="زبان و ادبیات فارسی",
                    educational_records=[
                        EducationalRecord(title=cells[4].text.strip())
                    ],
                    college="ادبیات و علوم انسانی ",
                )
                yield professor
    except:
        pass


# ادبیات علوم انسانی -  زبان و ادبیات عرب
def get_ensani__zaban_arab_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://ctb.iau.ir/literature/fa/page/1918/%D8%B2%D8%A8%D8%A7%D9%86-%D9%88-%D8%A7%D8%AF%D8%A8%DB%8C%D8%A7%D8%AA-%D8%B9%D8%B1%D8%A8"
        )
        page.wait_for_selector("table")
        content = page.content()
        browser.close()
    soup = BeautifulSoup(content, "html.parser")
    table = soup.find("table")
    if table is None:
        return
    try:
        for row in table.find("tbody").find_all("tr"):
            cells = row.find_all("td")
            professor = Professor(
                full_name=cells[1].text.strip(),
                rank=cells[3].text.strip(),
                group="زبان و ادبیات عرب",
                educational_records=[EducationalRecord(title=cells[4].text.strip())],
                college="ادبیات و علوم انسانی ",
            )
            yield professor
    except:
        pass


#  اقتصاد و حسابداری - گروه حسابداری
def get_eghtesad__hesabdari_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://ctb.iau.ir/eco/fa/page/2005/%DA%AF%D8%B1%D9%88%D9%87-%D8%AD%D8%B3%D8%A7%D8%A8%D8%AF%D8%A7%D8%B1%DB%8C"
        )
        page.wait_for_selector("table")
        content = page.content()
        browser.close()

    soup = BeautifulSoup(content, "html.parser")
    tbody_elements = soup.find_all("tbody")

    try:
        for tbody in tbody_elements:
            rows = tbody.find_all("tr")
            for row in rows:
                cells = row.find_all("td")

                if len(cells) >= 3 and cells[1].get_text(strip=True):
                    name = cells[1].get_text(strip=True)
                    rank = cells[2].get_text(strip=True)
                    if name:
                        professor = Professor(
                            full_name=name,
                            rank=rank,
                            group="حسابداری",
                            college="اقتصاد و حسابداری",
                        )
                        yield professor
    except:
        pass


#  اقتصاد و حسابداری - گروه اقتصاد بازرگانی و حمل ونقل
def get_eghtesad__bazargani_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://ctb.iau.ir/eco/fa/page/2004/%DA%AF%D8%B1%D9%88%D9%87-%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF-%D8%A8%D8%A7%D8%B2%D8%B1%DA%AF%D8%A7%D9%86%DB%8C-%D9%88-%D8%AD%D9%85%D9%84-%D9%88%D9%86%D9%82%D9%84"
        )
        page.wait_for_selector("table")
        content = page.content()
        browser.close()

    soup = BeautifulSoup(content, "html.parser")
    tbody_elements = soup.find_all("tbody")

    try:
        for tbody in tbody_elements:
            rows = tbody.find_all("tr")
            for row in rows:
                cells = row.find_all("td")

                if len(cells) >= 3 and cells[1].get_text(strip=True):
                    name = cells[1].get_text(strip=True)
                    rank = cells[2].get_text(strip=True)
                    if name:
                        professor = Professor(
                            full_name=name,
                            rank=rank,
                            group="بازرگانی و حمل و نقل",
                            college="اقتصاد و حسابداری",
                        )
                        yield professor
    except:
        pass


#  اقتصاد و حسابداری - گروه اقتصاد نظری و صنعتی
def get_eghtesad__nazari_sanati_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://ctb.iau.ir/eco/fa/page/2003/%DA%AF%D8%B1%D9%88%D9%87-%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF-%D9%86%D8%B8%D8%B1%DB%8C-%D9%88-%D8%B5%D9%86%D8%B9%D8%AA%DB%8C"
        )
        page.wait_for_selector("table")
        content = page.content()
        browser.close()

    soup = BeautifulSoup(content, "html.parser")
    tbody_elements = soup.find_all("tbody")

    try:
        for tbody in tbody_elements:
            rows = tbody.find_all("tr")
            for row in rows:
                cells = row.find_all("td")

                if len(cells) >= 3 and cells[1].get_text(strip=True):
                    name = cells[1].get_text(strip=True)
                    rank = cells[2].get_text(strip=True)
                    if name:
                        professor = Professor(
                            full_name=name,
                            rank=rank,
                            group="اقتصاد نظری و صنعتی",
                            college="اقتصاد و حسابداری",
                        )
                        yield professor
    except:
        pass


#   تربیت بدنی - علوم ورزشی
def get_tarbiat_badani__olum_varzeshi_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://ctb.iau.ir/sport/fa/page/5380/%D9%85%D8%AF%DB%8C%D8%B1%DB%8C%D8%AA-%D9%88%D8%B1%D8%B2%D8%B4%DB%8C"
        )
        page.wait_for_selector("table")
        content = page.content()
        browser.close()

    soup = BeautifulSoup(content, "html.parser")
    table = soup.find(
        "table", {"border": "0", "cellpadding": "1", "cellspacing": "1", "width": "289"}
    )
    try:
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) > 1:
                name = cells[0].get_text(strip=True)
                rank = cells[1].get_text(strip=True)
                if name:
                    professor = Professor(
                        full_name=name,
                        rank=rank,
                        group="علوم ورزشی",
                        college="تربیت بدنی",
                    )
                    yield professor
    except:
        pass


#   تربیت بدنی -  رفتار حرکتی
def get_tarbiat_badani__raftar_harkati_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://ctb.iau.ir/sport/fa/page/5379/%D8%B1%D9%81%D8%AA%D8%A7%D8%B1-%D8%AD%D8%B1%DA%A9%D8%AA%DB%8C"
        )
        page.wait_for_selector("table")
        content = page.content()
        browser.close()

    soup = BeautifulSoup(content, "html.parser")
    table = soup.find("tbody")
    try:
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) > 1:
                name = cells[0].get_text(strip=True)
                rank = cells[1].get_text(strip=True)
                if name:
                    professor = Professor(
                        full_name=name,
                        rank=rank,
                        group="رفتار حرکتی",
                        college="تربیت بدنی",
                    )
                    yield professor
    except:
        pass


#   تربیت بدنی -   فیزیولوژی ورزشی
def get_tarbiat_badani__physiology_varzeshi_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://ctb.iau.ir/sport/fa/page/5381/%D9%81%DB%8C%D8%B2%DB%8C%D9%88%D9%84%D9%88%DA%98%DB%8C-%D9%88%D8%B1%D8%B2%D8%B4%DB%8C"
        )
        page.wait_for_selector("table")
        content = page.content()
        browser.close()

    soup = BeautifulSoup(content, "html.parser")
    table = soup.find("tbody")

    try:
        rows = table.find_all("tr")[1:]
        for row in rows:
            cells = row.find_all("td")
            if len(cells) > 1:
                name = cells[0].get_text(strip=True)
                rank = cells[1].get_text(strip=True)
                if name:
                    professor = Professor(
                        full_name=name,
                        rank=rank,
                        group="فیزیولوژی ورزشی",
                        college="تربیت بدنی",
                    )
                    yield professor
    except:
        pass


#   تربیت بدنی -   فیزیولوژی ورزشی
def get_tarbiat_badani__physiology_varzeshi_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://ctb.iau.ir/sport/fa/page/5381/%D9%81%DB%8C%D8%B2%DB%8C%D9%88%D9%84%D9%88%DA%98%DB%8C-%D9%88%D8%B1%D8%B2%D8%B4%DB%8C"
        )
        page.wait_for_selector("table")
        content = page.content()
        browser.close()

    soup = BeautifulSoup(content, "html.parser")
    table = soup.find("tbody")

    try:
        rows = table.find_all("tr")[1:]
        for row in rows:
            cells = row.find_all("td")
            if len(cells) > 1:
                name = cells[0].get_text(strip=True)
                rank = cells[1].get_text(strip=True)
                if name:
                    professor = Professor(
                        full_name=name,
                        rank=rank,
                        group="فیزیولوژی ورزشی",
                        college="تربیت بدنی",
                    )
                    yield professor
    except:
        pass


#   تربیت بدنی -    بیومکانیک ورزشی
def get_tarbiat_badani__biomechanic_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://ctb.iau.ir/sport/fa/page/5382/%D8%A8%DB%8C%D9%88%D9%85%DA%A9%D8%A7%D9%86%DB%8C%DA%A9-%D9%88%D8%B1%D8%B2%D8%B4%DB%8C"
        )
        page.wait_for_selector("table")
        content = page.content()
        browser.close()

    soup = BeautifulSoup(content, "html.parser")
    table = soup.find("tbody")

    try:
        rows = table.find_all("tr")[1:]
        for row in rows:
            cells = row.find_all("td")
            if len(cells) > 1:
                name = cells[0].get_text(strip=True)
                rank = cells[1].get_text(strip=True)
                if name:
                    professor = Professor(
                        full_name=name,
                        rank=rank,
                        group="بیومکانیک ورزشی",
                        college="تربیت بدنی",
                    )
                    yield professor
    except:
        pass


#    هنر - نمایش
def get_honar__namayesh_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://ctb.iau.ir/art/fa/page/2323/%D8%A7%D8%B9%D8%B6%D8%A7%DB%8C-%D9%87%DB%8C%D8%A7%D8%AA-%D8%B9%D9%84%D9%85%DB%8C"
        )
        page.wait_for_selector("table")
        content = page.content()
        browser.close()

    soup = BeautifulSoup(content, "html.parser")
    tbody = soup.find('tbody')
    if tbody:
        rows = tbody.find_all('tr')[1:]
        try:  
            for row in rows:
                cells = row.find_all("td")
                if len(cells) >= 4: 
                    name = cells[1].get_text(strip=True)
                    major = cells[2].get_text(strip=True)
                    email = cells[3].get_text(strip=True)

                    professor = Professor(
                                full_name=name,
                                major=major,
                                group="نمایش",
                                college="هنر", 
                            )
                    professor.email.append(email)
                    yield professor
        except:
            pass



#    هنر -  موسیقی
def get_honar__music_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://ctb.iau.ir/art/fa/page/2307/%D8%A7%D8%B9%D8%B6%D8%A7%DB%8C-%D9%87%DB%8C%D8%A7%D8%AA-%D8%B9%D9%84%D9%85%DB%8C"
        )
        page.wait_for_selector("table")
        content = page.content()
        browser.close()

    soup = BeautifulSoup(content, "html.parser")
    tbody = soup.find('tbody')
    if tbody:
        rows = tbody.find_all('tr')[1:]
        try:  
            for row in rows:
                cells = row.find_all("td")
                if len(cells) >= 4: 
                    name = cells[1].get_text(strip=True)
                    major = cells[2].get_text(strip=True)
                    email = cells[3].get_text(strip=True)

                    professor = Professor(
                                full_name=name,
                                major=major,
                                group=" موسیقی",
                                college="هنر", 
                            )
                    professor.email.append(email)
                    yield professor
        except:
            pass


#    هنر -  نقاشی
def get_honar__naghashi_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://ctb.iau.ir/art/fa/page/2315/%D8%A7%D8%B9%D8%B6%D8%A7%DB%8C-%D9%87%DB%8C%D8%A7%D8%AA-%D8%B9%D9%84%D9%85%DB%8C"
        )
        page.wait_for_selector("table")
        content = page.content()
        browser.close()

    soup = BeautifulSoup(content, "html.parser")
    tbody = soup.find('tbody')
    if tbody:
        rows = tbody.find_all('tr')[1:]
        try:  
            for row in rows:
                cells = row.find_all("td")
                if len(cells) >= 4: 
                    name = cells[1].get_text(strip=True)
                    major = cells[2].get_text(strip=True)
                    email = cells[3].get_text(strip=True)

                    professor = Professor(
                                full_name=name,
                                major=major,
                                group=" نقاشی",
                                college="هنر", 
                            )
                    professor.email.append(email)
                    yield professor
        except:
            pass


#    هنر -  عکاسی
def get_honar__akasi_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://ctb.iau.ir/art/fa/page/2275/%D8%A7%D8%B9%D8%B6%D8%A7%DB%8C-%D9%87%DB%8C%D8%A7%D8%AA-%D8%B9%D9%84%D9%85%DB%8C"
        )
        page.wait_for_selector("table")
        content = page.content()
        browser.close()

    soup = BeautifulSoup(content, "html.parser")
    tbody = soup.find('tbody')
    if tbody:
        rows = tbody.find_all('tr')[1:]
        try:  
            for row in rows:
                cells = row.find_all("td")
                if len(cells) >= 4: 
                    name = cells[1].get_text(strip=True)
                    major = cells[2].get_text(strip=True)
                    email = cells[3].get_text(strip=True)

                    professor = Professor(
                                full_name=name,
                                major=major,
                                group=" عکاسی",
                                college="هنر", 
                            )
                    professor.email.append(email)
                    yield professor
        except:
            pass


#    هنر -  طراحی صنعتی
def get_honar__tarahi_sanati_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://ctb.iau.ir/art/fa/page/2259/%D8%A7%D8%B9%D8%B6%D8%A7%DB%8C-%D9%87%DB%8C%D8%A7%D8%AA-%D8%B9%D9%84%D9%85%DB%8C"
        )
        page.wait_for_selector("table")
        content = page.content()
        browser.close()

    soup = BeautifulSoup(content, "html.parser")
    tbody = soup.find('tbody')
    if tbody:
        rows = tbody.find_all('tr')[1:]
        try:  
            for row in rows:
                cells = row.find_all("td")
                if len(cells) >= 4: 
                    name = cells[1].get_text(strip=True)
                    major = cells[2].get_text(strip=True)
                    email = cells[3].get_text(strip=True)

                    professor = Professor(
                                full_name=name,
                                major=major,
                                group=" طراحی صنعتی",
                                college="هنر", 
                            )
                    professor.email.append(email)
                    yield professor
        except:
            pass



#    هنر -   پژوهش هنر
def get_honar__pazhouhesh_honar_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://ctb.iau.ir/art/fa/page/2251/%D8%A7%D8%B9%D8%B6%D8%A7%DB%8C-%D9%87%DB%8C%D8%A7%D8%AA-%D8%B9%D9%84%D9%85%DB%8C"
        )
        page.wait_for_selector("table")
        content = page.content()
        browser.close()

    soup = BeautifulSoup(content, "html.parser")
    tbody = soup.find('tbody')
    if tbody:
        rows = tbody.find_all('tr')[1:]
        try:  
            for row in rows:
                cells = row.find_all("td")
                if len(cells) >= 4: 
                    name = cells[1].get_text(strip=True)
                    education = cells[2].get_text(strip=True)
                    email = cells[3].get_text(strip=True)

                    professor = Professor(
                                full_name=name,
                                group="پژوهش هنر",
                                college="هنر", 
                            )
                    professor.email.append(email)
                    professor.educational_records.append(education)
                    yield professor
        except:
            pass



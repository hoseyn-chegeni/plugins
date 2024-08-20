from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from schemas.professor import Professor, EducationalRecord


# ادبیات علوم انسانی -علوم قرآن و حدیث
def get_professors_1():
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
                educational_records=[
                    EducationalRecord(title=cells[4].text.strip())
                ],
                college= "ادبیات و علوم انسانی "
            )
            yield professor
    except:
        pass

# ادبیات علوم انسانی -   ادیان و عرفان اسلامی
def get_professors_2():
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
                educational_records=[
                    EducationalRecord(title=cells[4].text.strip())
                ],
                college= "ادبیات و علوم انسانی "
            )
            yield professor
    except:
        pass


# ادبیات علوم انسانی -   فقه و حقوق اسلامی
def get_professors_3():
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
                group= "فقه و حقوق اسلامی",
                educational_records=[
                    EducationalRecord(title=cells[4].text.strip())
                ],
                college= "ادبیات و علوم انسانی "
            )
            yield professor
    except:
        pass



# ادبیات علوم انسانی -  تاریخ و باستانشناسی
def get_professors_4():
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
                educational_records=[
                    EducationalRecord(title=cells[4].text.strip())
                ],
                college= "ادبیات و علوم انسانی "
            )
            yield professor
    except:
        pass



# ادبیات علوم انسانی -  فلسفه و حکمت اسلامی
def get_professors_5():
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
                educational_records=[
                    EducationalRecord(title=cells[4].text.strip())
                ],
                college= "ادبیات و علوم انسانی "
            )
            yield professor
    except:
        pass



# ادبیات علوم انسانی - فلسفه غرب
def get_professors_6():
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
                educational_records=[
                    EducationalRecord(title=cells[4].text.strip())
                ],
                college= "ادبیات و علوم انسانی "
            )
            yield professor
    except:
        pass


# ادبیات علوم انسانی -  جغرافیا

def get_professors_7():
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
                educational_records=[
                    EducationalRecord(title=cells[4].text.strip())
                ],
                college= "ادبیات و علوم انسانی "
            )
            yield professor
    except:
        pass


# ادبیات علوم انسانی -  زبان و ادبیات فارسی
def get_professors_8():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://ctb.iau.ir/literature/fa/page/1917/%D8%B2%D8%A8%D8%A7%D9%86-%D9%88-%D8%A7%D8%AF%D8%A8%DB%8C%D8%A7%D8%AA-%D9%81%D8%A7%D8%B1%D8%B3%DB%8C")
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
                    college="ادبیات و علوم انسانی "
                )
                yield professor
    except:
        pass


# ادبیات علوم انسانی -  زبان و ادبیات عرب
def get_professors_9():
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
                educational_records=[
                    EducationalRecord(title=cells[4].text.strip())
                ],
                college= "ادبیات و علوم انسانی "
            )
            yield professor
    except:
        pass

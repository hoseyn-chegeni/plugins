from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from schemas.professor import Professor


"""ازاد تهران شرق"""


# شیمی
def get_shimi_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://etb.iau.ir/oloompayeh/fa/page/330/%D8%A7%D8%B9%D8%B6%D8%A7%DB%8C-%D9%87%DB%8C%D8%A7%D8%AA-%D8%B9%D9%84%D9%85%DB%8C-%DA%AF%D8%B1%D9%88%D9%87-%D8%B4%DB%8C%D9%85%DB%8C"
        )
        page.wait_for_selector("tbody")
        page_content = page.content()
        browser.close()

    soup = BeautifulSoup(page_content, "html.parser")
    tbody = soup.find("tbody")
    rows = tbody.find_all("tr")
    for row in rows[1:]:
        cells = row.find_all("td")
        if len(cells) == 6:
            first_name = cells[1].get_text(strip=True)
            last_name = cells[2].get_text(strip=True)
            group = cells[3].get_text(strip=True)
            rank = cells[5].get_text(strip=True)
            professor = Professor(
                full_name=first_name + last_name, group=group, rank=rank
            )
            yield professor


# علوم پایه
def get_oloom_paye_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://etb.iau.ir/oloompayeh/fa/page/343/%D8%A7%D8%B9%D8%B6%D8%A7%DB%8C-%D9%87%DB%8C%D8%A7%D8%AA-%D8%B9%D9%84%D9%85%DB%8C-%DA%AF%D8%B1%D9%88%D9%87-%D8%B9%D9%84%D9%88%D9%85-%D9%BE%D8%A7%DB%8C%D9%87"
        )
        page.wait_for_selector("tbody")
        page_content = page.content()
        browser.close()
    soup = BeautifulSoup(page_content, "html.parser")
    tbody = soup.find("tbody")
    for row in tbody.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) == 6:

            name = cells[1].get_text(strip=True)
            group = cells[2].get_text(strip=True)
            major = cells[3].get_text(strip=True)
            rank = cells[5].get_text(strip=True)
            professor = Professor(full_name=name, rank=rank, major=major, group=group)
            yield professor


# زیست
def get_zist_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://etb.iau.ir/oloompayeh/fa/page/337/%D8%A7%D8%B9%D8%B6%D8%A7%DB%8C-%D9%87%DB%8C%D8%A7%D8%AA-%D8%B9%D9%84%D9%85%DB%8C-%DA%AF%D8%B1%D9%88%D9%87-%D8%B2%DB%8C%D8%B3%D8%AA-%D8%B4%D9%86%D8%A7%D8%B3%DB%8C"
        )
        page.wait_for_selector("ul")
        page_content = page.content()
        browser.close()

    soup = BeautifulSoup(page_content, "html.parser")
    table = soup.find(
        "table",
        {
            "align": "right",
            "border": "1",
            "cellpadding": "0",
            "cellspacing": "0",
            "dir": "rtl",
        },
    )
    rows = table.find_all("tr")
    for row in rows[1:]:
        cells = row.find_all("td")
        if len(cells) == 7:
            first_name = cells[1].get_text(strip=True)
            last_name = cells[2].get_text(strip=True)
            faculty = cells[3].get_text(strip=True)
            group = cells[4].get_text(strip=True)
            rank = cells[6].get_text(strip=True)

            professor = Professor(
                full_name=first_name + last_name,
                faculty=faculty,
                group=group,
                rank=rank,
            )
            yield professor


# مهندسی پزشکی
def get_mohandesi_pezeshki_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://etb.iau.ir/fani/fa/page/368/%D8%A7%D8%B9%D8%B6%D8%A7%DB%8C-%D9%87%DB%8C%D8%A7%D8%AA-%D8%B9%D9%84%D9%85%DB%8C-%DA%AF%D8%B1%D9%88%D9%87-%D8%A8%D8%B1%D9%82"
        )
        page.wait_for_selector("tbody")
        page_content = page.content()
        browser.close()
    soup = BeautifulSoup(page_content, "html.parser")
    tbody = soup.find("tbody")
    for row in tbody.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) == 6:

            name = cells[1].get_text(strip=True)
            group = cells[2].get_text(strip=True)
            major = cells[3].get_text(strip=True)
            rank = cells[5].get_text(strip=True)
            professor = Professor(full_name=name, rank=rank, major=major, group=group)
            yield professor


#  کامپبوتر
def get_computer_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://etb.iau.ir/fani/fa/page/375/%D8%A7%D8%B9%D8%B6%D8%A7%DB%8C-%D9%87%DB%8C%D8%A7%D8%AA-%D8%B9%D9%84%D9%85%DB%8C-%DA%AF%D8%B1%D9%88%D9%87-%DA%A9%D8%A7%D9%85%D9%BE%DB%8C%D9%88%D8%AA%D8%B1"
        )
        page.wait_for_selector("tbody")
        page_content = page.content()
        browser.close()
    soup = BeautifulSoup(page_content, "html.parser")
    tbody = soup.find("tbody")
    for row in tbody.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) == 6:

            name = cells[1].get_text(strip=True)
            group = cells[2].get_text(strip=True)
            major = cells[3].get_text(strip=True)
            rank = cells[5].get_text(strip=True)
            professor = Professor(full_name=name, rank=rank, major=major, group=group)
            yield professor


#   مهندسی عمران
def get_omran_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://etb.iau.ir/fani/fa/page/389/%D8%A7%D8%B9%D8%B6%D8%A7%DB%8C-%D9%87%DB%8C%D8%A7%D8%AA-%D8%B9%D9%84%D9%85%DB%8C-%DA%AF%D8%B1%D9%88%D9%87-%D8%B9%D9%85%D8%B1%D8%A7%D9%86"
        )
        page.wait_for_selector("tbody")
        page_content = page.content()
        browser.close()
    soup = BeautifulSoup(page_content, "html.parser")
    tbody = soup.find("tbody")
    for row in tbody.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) == 6:

            name = cells[1].get_text(strip=True)
            group = cells[2].get_text(strip=True)
            major = cells[3].get_text(strip=True)
            rank = cells[5].get_text(strip=True)
            professor = Professor(full_name=name, rank=rank, major=major, group=group)
            yield professor


# مهندسی مکانیک و مهندسی هوافضا
def get_hava_faza_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://etb.iau.ir/fani/fa/page/382/%D8%A7%D8%B9%D8%B6%D8%A7%DB%8C-%D9%87%DB%8C%D8%A7%D8%AA-%D8%B9%D9%84%D9%85%DB%8C-%DA%AF%D8%B1%D9%88%D9%87-%D9%85%DA%A9%D8%A7%D9%86%DB%8C%DA%A9"
        )
        page.wait_for_selector("tbody")
        page_content = page.content()
        browser.close()
    soup = BeautifulSoup(page_content, "html.parser")
    tbody = soup.find("tbody")
    for row in tbody.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) == 6:

            name = cells[1].get_text(strip=True)
            group = cells[2].get_text(strip=True)
            major = cells[3].get_text(strip=True)
            rank = cells[5].get_text(strip=True)
            professor = Professor(full_name=name, rank=rank, major=major, group=group)
            yield professor


# مدیریت
def get_modiriat_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://etb.iau.ir/oloomensani/fa/page/520/%D8%A7%D8%B9%D8%B6%D8%A7%DB%8C-%D9%87%DB%8C%D8%A7%D8%AA-%D8%B9%D9%84%D9%85%DB%8C-%DA%AF%D8%B1%D9%88%D9%87-%D9%85%D8%AF%DB%8C%D8%B1%DB%8C%D8%AA"
        )
        page.wait_for_selector("tbody")
        page_content = page.content()
        browser.close()

    soup = BeautifulSoup(page_content, "html.parser")
    tbody = soup.find("tbody")
    rows = tbody.find_all("tr")
    for row in rows[1:]:
        cells = row.find_all("td")
        if len(cells) == 6:
            first_name = cells[4].get_text(strip=True)
            last_name = cells[3].get_text(strip=True)
            group = cells[2].get_text(strip=True)
            rank = cells[0].get_text(strip=True)
            professor = Professor(
                full_name=first_name + " " + last_name, group=group, rank=rank
            )
            yield professor


# علوم اجتماعی
def get_oloom_ejtemaee_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://etb.iau.ir/oloomensani/fa/page/406/%D8%A7%D8%B9%D8%B6%D8%A7%DB%8C-%D9%87%DB%8C%D8%A7%D8%AA-%D8%B9%D9%84%D9%85%DB%8C-%DA%AF%D8%B1%D9%88%D9%87-%D8%B9%D9%84%D9%88%D9%85-%D8%A7%D8%B1%D8%AA%D8%A8%D8%A7%D8%B7%D8%A7%D8%AA-%D9%88-%D8%B9%D9%84%D9%88%D9%85-%D8%A7%D8%AC%D8%AA%D9%85%D8%A7%D8%B9%DB%8C"
        )
        page.wait_for_selector("tbody")
        page_content = page.content()
        browser.close()

    soup = BeautifulSoup(page_content, "html.parser")
    tbody = soup.find("tbody")
    rows = tbody.find_all("tr")
    for row in rows[1:]:
        cells = row.find_all("td")
        if len(cells) == 5:
            first_name = cells[1].get_text(strip=True)
            last_name = cells[2].get_text(strip=True)
            rank = cells[4].get_text(strip=True)
            professor = Professor(
                full_name=first_name + " " + last_name,
                rank=rank,
                group="علوم ارتباطات و علوم اجتماعی",
            )
            yield professor


# تربیت بدنی
def get_tarbiat_badain_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://etb.iau.ir/oloomensani/fa/page/413/%D8%A7%D8%B9%D8%B6%D8%A7%DB%8C-%D9%87%DB%8C%D8%A3%D8%AA-%D8%B9%D9%84%D9%85%DB%8C-%DA%AF%D8%B1%D9%88%D9%87-%D8%B9%D9%84%D9%88%D9%85-%D9%88%D8%B1%D8%B2%D8%B4%DB%8C"
        )
        page.wait_for_selector("tbody")
        page_content = page.content()
        browser.close()

    soup = BeautifulSoup(page_content, "html.parser")
    tbody = soup.find("tbody")
    rows = tbody.find_all("tr")
    for row in rows[1:]:
        cells = row.find_all("td")
        if len(cells) == 7:
            first_name = cells[1].get_text(strip=True)
            last_name = cells[2].get_text(strip=True)
            group = cells[3].get_text(strip=True)
            major = cells[4].get_text(strip=True)
            rank = cells[6].get_text(strip=True)
            professor = Professor(
                full_name=first_name + " " + last_name,
                group=group,
                major=major,
                rank=rank,
            )
            yield professor


# حسابداری
def get_hesabdari_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://etb.iau.ir/oloomensani/fa/page/422/%D8%A7%D8%B9%D8%B6%D8%A7%DB%8C-%D9%87%DB%8C%D8%A7%D8%AA-%D8%B9%D9%84%D9%85%DB%8C-%DA%AF%D8%B1%D9%88%D9%87-%D8%AD%D8%B3%D8%A7%D8%A8%D8%AF%D8%A7%D8%B1%DB%8C"
        )
        page.wait_for_selector("tbody")
        page_content = page.content()
        browser.close()

    soup = BeautifulSoup(page_content, "html.parser")
    tbody = soup.find("tbody")
    rows = tbody.find_all("tr")
    for row in rows[1:]:
        cells = row.find_all("td")
        first_name = cells[1].get_text(strip=True)
        last_name = cells[2].get_text(strip=True)
        group = cells[3].get_text(strip=True)
        major = cells[4].get_text(strip=True)
        rank = cells[6].get_text(strip=True)
        professor = Professor(
            full_name=first_name + " " + last_name, group=group, major=major, rank=rank
        )
        yield professor


# حقوق
def get_hoquq_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://etb.iau.ir/oloomensani/fa/page/431/%D8%A7%D8%B9%D8%B6%D8%A7%DB%8C-%D9%87%DB%8C%D8%A7%D8%AA-%D8%B9%D9%84%D9%85%DB%8C-%DA%AF%D8%B1%D9%88%D9%87-%D8%AD%D9%82%D9%88%D9%82"
        )
        page.wait_for_selector("tbody")
        page_content = page.content()
        browser.close()

    soup = BeautifulSoup(page_content, "html.parser")
    tbody = soup.find("tbody")
    rows = tbody.find_all("tr")
    for row in rows[1:]:
        cells = row.find_all("td")
        first_name = cells[1].get_text(strip=True)
        last_name = cells[2].get_text(strip=True)
        group = cells[3].get_text(strip=True)
        major = cells[4].get_text(strip=True)
        rank = cells[6].get_text(strip=True)
        professor = Professor(
            full_name=first_name + " " + last_name, group=group, major=major, rank=rank
        )
        yield professor


# ادبیات
def get_adabiat_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://etb.iau.ir/oloomensani/fa/page/445/%D8%A7%D8%B9%D8%B6%D8%A7%DB%8C-%D9%87%DB%8C%D8%A7%D8%AA-%D8%B9%D9%84%D9%85%DB%8C-%DA%AF%D8%B1%D9%88%D9%87-%D8%A7%D8%AF%D8%A8%DB%8C%D8%A7%D8%AA-%D9%81%D8%A7%D8%B1%D8%B3%DB%8C-%D9%88-%D8%AF%D8%B1%D9%88%D8%B3-%D8%B9%D9%85%D9%88%D9%85%DB%8C"
        )
        page.wait_for_selector("tbody")
        page_content = page.content()
        browser.close()

    soup = BeautifulSoup(page_content, "html.parser")
    tbody = soup.find("tbody")
    rows = tbody.find_all("tr")
    for row in rows[1:]:
        cells = row.find_all("td")
        first_name = cells[1].get_text(strip=True)
        last_name = cells[2].get_text(strip=True)
        group = cells[3].get_text(strip=True)
        major = cells[4].get_text(strip=True)
        rank = cells[6].get_text(strip=True)
        professor = Professor(
            full_name=first_name + " " + last_name, group=group, major=major, rank=rank
        )
        yield professor


# معارف اسلامی
def get_maaref_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://etb.iau.ir/oloomensani/fa/page/452/%D8%A7%D8%B9%D8%B6%D8%A7%DB%8C-%D9%87%DB%8C%D8%A7%D8%AA-%D8%B9%D9%84%D9%85%DB%8C-%DA%AF%D8%B1%D9%88%D9%87-%D9%85%D8%B9%D8%A7%D8%B1%D9%81-%D8%A7%D8%B3%D9%84%D8%A7%D9%85%DB%8C"
        )
        page.wait_for_selector("tbody")
        page_content = page.content()
        browser.close()

    soup = BeautifulSoup(page_content, "html.parser")
    tbody = soup.find("tbody")
    rows = tbody.find_all("tr")
    for row in rows[1:]:
        cells = row.find_all("td")
        first_name = cells[1].get_text(strip=True)
        last_name = cells[2].get_text(strip=True)
        major = cells[3].get_text(strip=True)
        rank = cells[5].get_text(strip=True)
        professor = Professor(
            full_name=first_name + " " + last_name, major=major, rank=rank
        )
        yield professor


#  هنر
def get_honar_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://etb.iau.ir/honar/fa/page/466/%D8%A7%D8%B9%D8%B6%D8%A7%DB%8C-%D9%87%DB%8C%D8%A7%D8%AA-%D8%B9%D9%84%D9%85%DB%8C-%DA%AF%D8%B1%D9%88%D9%87-%D9%87%D9%86%D8%B1"
        )
        page.wait_for_selector("tbody")
        page_content = page.content()
        browser.close()

    soup = BeautifulSoup(page_content, "html.parser")
    tbody = soup.find("tbody")
    rows = tbody.find_all("tr")
    for row in rows[1:]:
        cells = row.find_all("td")
        first_name = cells[1].get_text(strip=True)
        last_name = cells[2].get_text(strip=True)
        group = cells[4].get_text(strip=True)
        major = cells[4].get_text(strip=True)
        rank = cells[6].get_text(strip=True)
        professor = Professor(
            full_name=first_name + " " + last_name, major=major, rank=rank, group=group
        )

        yield professor


#  معماری
def get_memari_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://etb.iau.ir/honar/fa/page/473/%D8%A7%D8%B9%D8%B6%D8%A7%DB%8C-%D9%87%DB%8C%D8%A7%D8%AA-%D8%B9%D9%84%D9%85%DB%8C-%DA%AF%D8%B1%D9%88%D9%87-%D9%85%D8%B9%D9%85%D8%A7%D8%B1%DB%8C"
        )
        page.wait_for_selector("tbody")
        page_content = page.content()
        browser.close()

    soup = BeautifulSoup(page_content, "html.parser")
    tbody = soup.find("tbody")
    rows = tbody.find_all("tr")
    for row in rows[1:]:
        cells = row.find_all("td")
        first_name = cells[1].get_text(strip=True)
        last_name = cells[2].get_text(strip=True)
        group = cells[4].get_text(strip=True)
        major = cells[4].get_text(strip=True)
        rank = cells[6].get_text(strip=True)
        professor = Professor(
            full_name=first_name + " " + last_name, major=major, rank=rank, group=group
        )

        yield professor

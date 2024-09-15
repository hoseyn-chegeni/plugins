from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from schemas.professor import Professor


"""ازاد تهران شرق"""

# شیمی
def get_shimi_prof():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://etb.iau.ir/oloompayeh/fa/page/330/%D8%A7%D8%B9%D8%B6%D8%A7%DB%8C-%D9%87%DB%8C%D8%A7%D8%AA-%D8%B9%D9%84%D9%85%DB%8C-%DA%AF%D8%B1%D9%88%D9%87-%D8%B4%DB%8C%D9%85%DB%8C")
        page.wait_for_selector("tbody")  
        page_content = page.content()
        browser.close()

    soup = BeautifulSoup(page_content, 'html.parser')
    tbody = soup.find('tbody')
    rows = tbody.find_all('tr')
    for row in rows[1:]:
        cells = row.find_all('td')
        if len(cells) == 6: 
            first_name =  cells[1].get_text(strip=True)
            last_name =  cells[2].get_text(strip=True)
            group = cells[3].get_text(strip=True)
            rank = cells[5].get_text(strip=True)
            professor = Professor(full_name=first_name +last_name, group=group, rank=rank)
            yield professor



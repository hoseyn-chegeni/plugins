import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from crawlers.universities.chamran_ahvaz import ChamranAhvazCrawler
from crawlers.universities.elm_sanat import ElmSanatCrawler
from crawlers.universities.sanati_qome import QUTCrawler

""" چمران اهواز """
crawler = ChamranAhvazCrawler()
for college in crawler.get_colleges():
    print(college)


""" علم و صنعت """
# def main():
#     crawler = ElmSanatCrawler()
#     professor_links = crawler.get_professors()
#     if not professor_links:
#         print("No professor links found.")
#         return

#     for link in professor_links:
#         professor_data = crawler.get_professor_page(link)
#         if professor_data:
#             print(professor_data)
#         else:
#             print(f"Failed to get data for link: {link}")

#     # employee
#     emp = crawler.get_employees()

#     # college
#     college = crawler.get_colleges()


""" صنعتی قم """


# def main():
#     crawler = QUTCrawler()
#     prof = crawler.get_professors()


#     # employee
#     emp = crawler.get_employees()

#     # college
#     college = crawler.get_colleges()


import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from crawlers.universities.chamran_ahvaz import ChamranAhvazCrawler
from crawlers.universities.elm_sanat import ElmSanatCrawler
from crawlers.universities.sanati_qome import QUTCrawler
from crawlers.universities.azad.tehran_markaz import TehranMarkazCrawler
from crawlers.universities.azad.tehran_qarb import TehranQarbCrawler
from crawlers.universities.azad.tehran_shomal import TehranShomalCrawler


""" چمران اهواز """
crawler = ChamranAhvazCrawler()
"""College"""
# for college in crawler.get_colleges():
#     print(college)
"""Employee"""
# for emp in crawler.get_employees():
#     print(emp)
"""Professor"""
# professor_links = crawler.get_professors()
# if not professor_links:
#     print("No professor links found.")

# for link in professor_links:
#     professor_data = crawler.get_professor_page(link)
#     if professor_data:
#         print(professor_data)
#     else:
#         print(f"Failed to get data for link: {link}")


""" علم و صنعت """
crawler = ElmSanatCrawler()
"""College"""
# for college in crawler.get_colleges():
#     print(college)
"""Employee"""
# for emp in crawler.get_employees():
#     print(emp)
"""Professor"""
# professor_links = crawler.get_professors()
# if not professor_links:
#     print("No professor links found.")

# for link in professor_links:
#     professor_data = crawler.get_professor_page(link)
#     if professor_data:
#         print(professor_data)
#     else:
#         print(f"Failed to get data for link: {link}")


""" صنعتی قم """
crawler = QUTCrawler()
"""College"""
# for college in crawler.get_colleges():
#     print(college)
"""Employee"""
#
"""Professor"""
# for professor in crawler.get_professors():
#     print(professor.group)


"""آزاد تهران مرکز"""
crawler = TehranMarkazCrawler()
"""College"""
# for college in crawler.get_colleges():
#     print(college)
"""Employee"""
# for emp in crawler.get_employees():
#     print(emp)
"""Professor"""
# crawler.get_professors()


"""آزاد تهران غرب"""
crawler = TehranQarbCrawler()
"""College"""
# for college in crawler.get_colleges():
#     print(college)
"""Employee"""
# for emp in crawler.get_employees():
#     print(emp)
"""Professor"""
# test = crawler.get_professor_page("")
# print(test)


"""آزاد تهران شمال"""
crawler = TehranShomalCrawler()
"""College"""
for college in crawler.get_colleges():
    print(college)
"""Employee"""
# for emp in crawler.get_employees():
#     print(emp)
"""Professor"""
# test = crawler.get_professor_page("https://ntb.iau.ir/faculty/ebnetorab/fa")
# print(test.full_name, test.rank, test.faculty, test.group, test.socials.personal_cv)

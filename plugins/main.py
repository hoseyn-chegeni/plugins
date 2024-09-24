import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from crawlers.universities.chamran_ahvaz import ChamranAhvazCrawler
from crawlers.universities.elm_sanat import ElmSanatCrawler
from crawlers.universities.sanati_qome import QUTCrawler
from crawlers.universities.azad.tehran.markaz import TehranMarkazCrawler
from crawlers.universities.azad.tehran.qarb import TehranQarbCrawler
from crawlers.universities.azad.tehran.shomal import TehranShomalCrawler
from crawlers.universities.azad.tehran.jonub import TehranJonubCrawler
from crawlers.universities.azad.tehran.shargh import TehranSharghCrawler
from crawlers.universities.azad.tehran.qods import QodsCrawler
from crawlers.universities.azad.aligodarz import AligodarzCrawler 



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
# for college in crawler.get_colleges():
#     print(college)
"""Employee"""
# for emp in crawler.get_employees():
#     print(emp)
"""Professor"""
# test = crawler.get_professor_page("https://ntb.iau.ir/faculty/ebnetorab/fa")
# print(test.full_name, test.rank, test.faculty, test.group, test.socials.personal_cv)


"""آزاد تهران جنوب"""
crawler = TehranJonubCrawler()
"""College"""
# for college in crawler.get_colleges():
#     print(college)
"""Employee"""
# for emp in crawler.get_employees():
#     print(emp)
"""Professor"""
# test = crawler.get_professor_page("https://stb.iau.ir/faculty/h-abniki/fa")
# print(test.full_name, test.rank, test.faculty, test.group, test.socials.personal_cv)


"""آزاد تهران شرق"""
crawler = TehranSharghCrawler()
"""College"""
# for college in crawler.get_colleges():
#     print(college)
"""Employee"""
# for emp in crawler.get_employees():
#     print(emp)
"""Professor"""
# for i in crawler.get_professors():
#     print(i)


"""آزاد  شهر قدس"""
crawler = QodsCrawler()
"""College"""
# for college in crawler.get_colleges():
#     print(college)
"""Employee"""
# for emp in crawler.get_employees():
#     print(emp)
"""Professor"""
# for i in crawler.get_professors():
#     print(i)


"""ali godarz"""
crawler = AligodarzCrawler()
"""College"""
for college in crawler.get_colleges():
    print(college)
"""Employee"""
# for emp in crawler.get_employees():
#      print(emp)
"""Professor"""
# for i in crawler.get_professors():
#     print(i.full_name)
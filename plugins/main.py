import sys
import os

# Add the parent directory to the sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from crawlers.universities.chamran_ahvaz import ChamranAhvazCrawler


def main():
    crawler = ChamranAhvazCrawler()

    # professor_links = crawler.get_professors()
    # if not professor_links:
    #     print("No professor links found.")
    #     return

    # for link in professor_links:
    #     professor_data = crawler.get_professor_page(link)
    #     if professor_data:
    #         print(professor_data)
    #     else:
    #         print(f"Failed to get data for link: {link}")

    # employee
    emp = crawler.get_colleges()



if __name__ == "__main__":
    main()

import sys
import os

# Add the parent directory to the sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from crawlers.universities.sanati_qome import QUTCrawler


def main():
    crawler = QUTCrawler()
    for college in crawler.get_colleges():
        print(college)


if __name__ == "__main__":
    main()

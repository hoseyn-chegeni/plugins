from requests import get
from bs4 import BeautifulSoup

from core.helper import helper
from core.enums.uni_beheshti import Degrees
from database.mongo.uni_beheshti import mongo_beheshti


class UniBeheshti:

    def __init__(self, use_cache: bool = False) -> None:
        """
        `use_cache`
            To use existing cursor or not
        """
        self.use_cache = use_cache
        self.base_url = "https://www.sbu.ac.ir"
        self.payloads = {}
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        }
        self.params = {
            'p_p_id': 'ir_sain_university_people_UniversityFacultyListPortlet',
            'p_p_lifecycle': 0,
            'p_p_state': 'normal',
            'p_p_mode': 'view',
            '_ir_sain_university_people_UniversityFacultyListPortlet_universityDepartmentId': 0,
            '_ir_sain_university_people_UniversityFacultyListPortlet_currentNumberPage': 0,
            '_ir_sain_university_people_UniversityFacultyListPortlet_universityProgramId': 0
        }

    def __activities(self, profile_id: str):
        source = BeautifulSoup(get(url=f"{self.base_url}/~{profile_id}/activities", data=self.payloads).text, 'html.parser')
        activities = source.find('section', {'class': 'main'}).find_all('li')
        for activity in activities:
            title = activity.find('span', {'class': 'title'})
            subtitle_label = activity.find('span', {'class': 'subtitle label'})
            date = activity.find('span', {'class': 'years'})
            start = None
            end = None
            if date:
                if date.text:
                    start = int(date.text.split('←')[0]) if date.text.split('←')[0].isdigit() else date.text.split('←')[0].strip()
                    end = int(date.text.split('←')[1]) if date.text.split('←')[1].isdigit() else date.text.split('←')[1].strip()
                    
            yield {
                'Title': title.text.strip() if title else None,
                'SubtitleLabel': subtitle_label.text.strip() if subtitle_label else None,
                'Start': start,
                'End': end
            }

    def __articles(self, profile_id: str):
        source = BeautifulSoup(get(url=f"{self.base_url}/~{profile_id}/articles", data=self.payloads).text, 'html.parser')
        articles = source.find('section', {'class': 'main'}).find_all('li', {'class': 'col-12 li-en'})
        for article in articles:
            data = article.find('span', {'class': 'subtitle subtitle-en'}).contents
            try:
                yield {
                    'Title': article.find('span', {'class': 'title title-en'}).text.strip() if article.find('span', {'class': 'title title-en'}) else None,
                    'CoAuthors': [author.strip() for author in data[0].split(',') if author.strip()] if data[0] else [],
                    'Description': article.find('em').text.strip() if article.find('em') else None,
                    'Volume': data[-3].text.strip().replace('\t', '').replace('\n', '') if data[-3] else None,
                    'Date': int(data[-2].text) if data[-2] else None
                }

            except:
                yield article.find('span', {'class': 'subtitle subtitle-en'}).text.strip().replace('\n', ' ').replace('\t', ' ')

    def __courses(self, profile_id: str, new_courses: bool = True):
        source = BeautifulSoup(get(url=f"{self.base_url}/~{profile_id}/courses", data=self.payloads).text, 'html.parser')
        if new_courses:
            base = source.find('div', {'class': 'container edu-list'})
            if base:
                courses_body = base.find('tbody')
                courses = courses_body.find_all('tr') if courses_body else None
                if courses:
                    for course in courses:
                        data = course.contents
                        yield {
                            'Name': data[1].text.strip(),
                            'Units': float(data[3].text),
                            'PresentationTime': data[5].text.strip(),
                            'Term': data[7].text.strip().replace('\u200c', '')
                        }
            else:
                courses = source.find_all('span', {'class': 'title'})
                if courses:
                    for course in courses:
                        yield {
                            'Name': course.text.strip().replace('\u200c', '')
                        }

    def __thesises(self, profile_id: str, degree: Degrees):
        source = BeautifulSoup(get(url=f"{self.base_url}/~{profile_id}/thesis", data=self.payloads).text, 'html.parser')

        if degree == Degrees.Doctoral:
            thesises_body = source.find('h2', text='رساله های دکتری')
            if thesises_body:
                try:
                    thesises = thesises_body.find_next_sibling('ol').find_all('li')
                except:
                    thesises = thesises_body.find_next_sibling('div', {'class': 'edu-list'}).find('ol').find_all('li')
                if thesises:
                    for thesis in thesises:
                        yield {
                            'Title': thesis.find('span', {'class': 'title'}).text.strip().replace('\u200c', ' '),
                            'Subtitle': thesis.find('span', {'class': 'subtitle'}).text.strip().replace('\u200c', ' '),
                            'Year': int(thesis.find('span', {'class': 'years'}).text)
                        }

        elif degree == Degrees.Master:
            thesises_body = source.find('h2', text='پایان‌نامه‌های کارشناسی‌ارشد')
            if thesises_body:
                try:
                    thesises = thesises_body.find_next_sibling('ol').find_all('li')
                except:
                    thesises = thesises_body.find_next_sibling('div', {'class': 'edu-list'}).find('ol').find_all('li')
                if thesises:
                    for thesis in thesises:
                        yield {
                            'Title': thesis.find('span', {'class': 'title'}).text.strip().replace('\u200c', ' '),
                            'Subtitle': thesis.find('span', {'class': 'subtitle'}).text.strip().replace('\u200c', ' '),
                            'Year': int(thesis.find('span', {'class': 'years'}).text)
                        }
        
        elif degree == Degrees.Bachelor:
            thesises_body = source.find('h2', text='پایان‌نامه‌های کارشناسی‌')
            if thesises_body:
                try:
                    thesises = thesises_body.find_next_sibling('ol').find_all('li')
                except:
                    thesises = thesises_body.find_next_sibling('div', {'class': 'edu-list'}).find('ol').find_all('li')
                if thesises:
                    for thesis in thesises:
                        yield {
                            'Title': thesis.find('span', {'class': 'title'}).text.strip().replace('\u200c', ' '),
                            'Subtitle': thesis.find('span', {'class': 'subtitle'}).text.strip().replace('\u200c', ' '),
                            'Year': int(thesis.find('span', {'class': 'years'}).text)
                        }

    def __books(self, profile_id: str):
        source = BeautifulSoup(get(url=f"{self.base_url}/~{profile_id}/books", data=self.payloads).text, 'html.parser')
        books = source.find_all('li', {'class': 'col-12 li-fa'})
        if books:
            for book in books:
                data = book.find('span', {'class': 'subtitle'}).contents
                yield {
                    'Title': book.find('span', {'class': 'title'}).text.replace('\u200c', ' ').strip(),
                    'Year': int(book.find('span', {'class': 'years'}).text.replace('،', '')) if book.find('span', {'class': 'years'}) else None,
                    'University': data[3].text.split('-')[0].replace('دانشگاه', '').replace('\u200c', ' ').strip(),
                    'ISBN': data[-1].text.replace('\u200c', ' ').strip().replace('شابک: ', '')
                }

    def __researchs(self, profile_id: str):
        source = BeautifulSoup(get(url=f"{self.base_url}/~{profile_id}/research", data=self.payloads).text, 'html.parser')
        researchs_body = source.find('h2', text=' ارتباط با صنعت')
        researchs = researchs_body.find_next_sibling('ol').find_all('li') if researchs_body else None
        if researchs:
            for research in researchs:
                yield {
                    'Title': research.find('span', {'class': 'title'}).text.replace('\u200c', ' ').strip(),
                    'Organization': research.find('span', {'class': 'subtitle'}).text.replace('\u200c', ' ').strip(),
                    'Year': int(research.find('span', {'class': 'years'}).text.replace('،', '')) if research.find('span', {'class': 'years'}) else None
                }

    def __prizes(self, profile_id: str):
        source = BeautifulSoup(get(url=f"{self.base_url}/~{profile_id}/award", data=self.payloads).text, 'html.parser')
        prizes_body = source.find('h2', text=' جوایز و افتخارات')
        prizes = prizes_body.find_next_sibling('ol').find_all('li') if prizes_body else None
        if prizes:
            for prize in prizes:
                yield {
                    'Title': prize.find('span', {'class': 'title'}).text.replace('\u200c', ' ').strip(),
                    'Year': int(prize.find('span', {'class': 'years'}).text.replace('،', '')) if prize.find('span', {'class': 'years'}) else None
                }

    def _complete_profile(self, profile_id: str):

        def _field_major(source: BeautifulSoup):
            field_major = source.find('h3', {'class': 'subtitle'}).text
            field = field_major.split('-')[0].strip().replace('\u200c', ' ').replace('\n', ' ').replace('\t', ' ')
            major = field_major.split('/')[0][len(field)+2:].strip().replace('\u200c', ' ')
            return field.split('/')[0].strip(), major.strip() if major else field.split('/')[1].strip()
        
        def _resume(source: BeautifulSoup):
            cv = source.find('a', {'class': 'cv'})
            if cv:
                return cv.attrs['href']

        def _last_update(source: BeautifulSoup):
            date = source.find('h6', {'class': 'content_modification-date'})
            if date:
                return str(helper.persian_to_datetime(date.text[19:]))

        def _view_count(source: BeautifulSoup):
            view_count = source.find('h6', {'class': 'view-count'})
            if view_count:
                return view_count.text[14:]

        def _education(source: BeautifulSoup):
            educations = source.find('ul', {'class': 'timeline'}).find_all('li')
            for education in educations:
                try:
                    data = education.contents[2].text.strip().replace('،', '').replace('-', '').split()
                    dates = education.find('span', {'class': 'years'}).text.strip().split('←') if education.find('span', {'class': 'years'}) else None
                    try:
                        yield {
                            'University': f"{data[1]} {data[2]}",
                            'City': data[3],
                            'Degree': education.find('span', {'class': 'code'}).text.replace(':', '').strip(),
                            'Field': f"{data[-3]} {data[-2]}" if len(data) == 7 else f"{data[-2]} {data[-1]}",
                            'Major': data[-1] if len(data) == 7 else None,
                            'Start': dates[0] if dates else None,
                            'End': dates[1] if dates else None
                        }
                    except:
                        yield {
                            'Data': data,
                            'Dates': dates
                        }
                except:
                    yield education.text.replace('\n', ' ').replace('\t', ' ').replace('\u200c', ' ')

        def _tags(source: BeautifulSoup):
            tags = source.find_all('span', {'class': 'tag'})
            if tags:
                return [tag.text.strip() for tag in tags]

        def _phone_number(source: BeautifulSoup):
            phone = source.find('b', text=' شماره تماس: ')
            if phone:
                number = phone.find_next_sibling('span')
                if number:
                    return int(number.text)

        def _email(source: BeautifulSoup):
            email = source.find('b', text=' رایانامه: ')
            if email:
                address = email.find_next_sibling('span')
                if address:
                    temp = address.text.split()
                    return f"{temp[0]}@{temp[2]}"

        source = BeautifulSoup(get(url=f"{self.base_url}/~{profile_id}", data=self.payloads).text, 'html.parser')
        field, major = _field_major(source)
        
        return {
            'Field': field,
            'Major': major,
            'Resume': _resume(source),
            'LastUpdate': _last_update(source),
            'ViewCount': _view_count(source),
            'Education': [e for e in _education(source)],
            'Tags': _tags(source),
            'PhoneNumber': _phone_number(source),
            'Email': _email(source),
            'Activities': [activity for activity in self.__activities(profile_id)],
            'Articles': [article for article in self.__articles(profile_id)],
            'Courses': {
                'Current': [course for course in self.__courses(profile_id)],
                'Previous': [course for course in self.__courses(profile_id, False)]
            },
            'Thesises': {
                'PHD': [thesis for thesis in self.__thesises(profile_id, Degrees.Doctoral)],
                'Master': [thesis for thesis in self.__thesises(profile_id, Degrees.Master)],
                'Bachelor': [thesis for thesis in self.__thesises(profile_id, Degrees.Bachelor)],
            },
            'Books': [book for book in self.__books(profile_id)],
            'Researchs': [research for research in self.__researchs(profile_id)],
            'Prizes': [prize for prize in self.__prizes(profile_id)]
        }

    def get_profiles(self):

        def _id(content: BeautifulSoup):
            return content.find('div', {'class': 'item'}).find('a').attrs['href'][2:]

        def _url(content: BeautifulSoup):
            return f"{self.base_url}{content.find('div', {'class': 'item'}).find('a').attrs['href']}"

        def _title(content: BeautifulSoup):
            return content.find('div', {'class': 'title'}).text.replace('\\u200c', ' ')

        def _degree(content: BeautifulSoup):
            return content.find('span', {'class': 'code'}).text

        def _sub_major(content: BeautifulSoup):
            return content.find('div', {'class': 'text'}).text.strip()

        def _image(content: BeautifulSoup):
            image_body = content.find('div', {'class': 'image'})
            if image_body:
                image = image_body.find('img', {'class': 'img'})
                if image:
                    if 'https://' in image.attrs['src']:
                        return image.attrs['src']
                    else:
                        return f"{self.base_url}{image.attrs['src']}"

        def _email(content: BeautifulSoup):
            attrs = content.find('a', {'class': 'email'})
            if attrs:
                return f"{attrs.attrs['data-email']}@{attrs.attrs['data-prefix']}"

        params = self.params.copy()

        while True:
            page = mongo_beheshti.load_page(self.use_cache)
            params['_ir_sain_university_people_UniversityFacultyListPortlet_currentNumberPage'] = page
            source = BeautifulSoup(get(url=f"{self.base_url}/cv", params=params, headers=self.headers, data=self.payloads).text, 'html.parser')
            if source.find('li', {'class': 'disabled page-item'}, text="بعد"): 
                mongo_beheshti.delete_page()
                break
            for content in source.find_all('div', {'class': 'col-md-6 col-xl-4'}):
                title = _title(content)
                profile_id = _id(content)
                profile = {
                    'Id': profile_id,
                    'Url': _url(content),
                    'Title': title,
                    'FirstName': title.split(maxsplit=1)[0].strip(),
                    'LastName': title.split(maxsplit=1)[1].strip(),
                    'Degree': _degree(content),
                    'SubMajor': _sub_major(content),
                    'Image': _image(content),
                    'Email': _email(content)
                }
                print(profile)
                profile.update(self._complete_profile(profile_id))
                yield profile
            mongo_beheshti.save_page(page+1)

from re import search
from requests import get
from bs4 import BeautifulSoup

from core.helper import helper
from core.enums.uni_tehran import SearchType
from database.mongo.uni_tehran import mongo_tehran


class UniTehran:

    def __init__(self, use_cache: bool = False) -> None:
        """
        `use_cache`
            To use existing cursor or not
        """
        self.use_cache = use_cache
        self.base_url = "https://profile.ut.ac.ir"
        self.payloads = {}
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-US,en;q=0.9,fa;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
        }
        self.params = {
            "p_p_id": "edusearch_WAR_edumanagerportlet_INSTANCE_PM4wXjldOANK",
            "p_p_lifecycle": 2,
            "p_p_state": "normal",
            "p_p_mode": "view",
            "p_p_cacheability": "cacheLevelPage",
            "p_p_col_id": "column-1",
            "p_p_col_count": 1,
            "currentFacet": "",
            "preFilter": False,
            "teacherTagIds": "",
            "thesisTagIds": "",
            "thesisDegree": "",
            "teacherId": "",
            "groupId": "",
            "thesisShamsiDefYears": "",
            "thesisDefYears": "",
            "type": "",
            "lang": "",
            "publishYear": "",
            "shmasiPublishYear": "",
            "startYear": "",
            "shamsiStartYear": "",
            "status": "",
            "enteranceYear": "",
            "areaOfStudyId": "",
            "page": 1,
            "index": "",
            "sortType": "",
            "userSortType": "",
            "tabSearchType": "",
            "currentSearchType": "",
            "searchType": "",
            "_edusearch_WAR_edumanagerportlet_INSTANCE_PM4wXjldOANK_keywords": "",
        }

    def get_journals(self):
        url = f"{self.base_url}/{SearchType.Journals.value}"
        params = self.params.copy()
        params["sortType"] = "publish-date"
        params["searchType"] = "student"

        while True:
            page = mongo_tehran.load_page(SearchType.Journals.name, self.use_cache)
            params["page"] = page
            response = get(
                url=url, params=params, headers=self.headers, data=self.payloads
            )
            if not response.text:
                break
            if not response.json().get("results", None):
                mongo_tehran.delete_page(SearchType.Journals.name)
                break
            else:
                for result in response.json()["results"]:
                    yield result
                mongo_tehran.save_page(SearchType.Journals.name, page + 1)

    def get_publications(self):
        url = f"{self.base_url}/{SearchType.Publications.value}"
        params = self.params.copy()
        params["sortType"] = "publish-date"
        params["searchType"] = "scholarly"

        while True:
            page = mongo_tehran.load_page(SearchType.Publications.name, self.use_cache)
            params["page"] = page
            response = get(
                url=url, params=params, headers=self.headers, data=self.payloads
            )
            if not response.text:
                break
            if not response.json().get("results", None):
                mongo_tehran.delete_page(SearchType.Publications.name)
                break
            else:
                for result in response.json()["results"]:
                    yield result
                mongo_tehran.save_page(SearchType.Publications.name, page + 1)

    def get_prizes(self):
        url = f"{self.base_url}/{SearchType.Prizes.value}"
        params = self.params.copy()
        params["sortType"] = "date"
        params["searchType"] = "prizes"

        while True:
            page = mongo_tehran.load_page(SearchType.Prizes.name, self.use_cache)
            params["page"] = page
            response = get(
                url=url, params=params, headers=self.headers, data=self.payloads
            )
            if not response.text:
                break
            if not response.json().get("results", None):
                mongo_tehran.delete_page(SearchType.Prizes.name)
                break
            else:
                for result in response.json()["results"]:
                    yield result
                mongo_tehran.save_page(SearchType.Prizes.name, page + 1)

    def complete_profile(self, profile_url: str):

        def _description(source: BeautifulSoup):
            descriptions = source.find_all("span", {"class": "centers"})
            if descriptions:
                return [_.text.strip() for _ in descriptions]
            else:
                return []

        def _major(source: BeautifulSoup):
            major = source.find("h6", {"class": "info-field teacher-collegeSubGgroup"})
            if major:
                return major.text.strip()
            else:
                return None

        def _phone_number(source: BeautifulSoup):
            info_fields = source.find_all("h6", {"class": "info-field"})

            if info_fields:
                for field in info_fields:
                    text = field.text
                    if "شماره تماس" in text:
                        match = search(r"([0-9]+)", text)
                        if match:
                            return match.group(1)

            return None

        def _room(source: BeautifulSoup):
            info_fields = source.find_all("h6", {"class": "info-field"})

            for field in info_fields:
                text = field.text
                if "اتاق" in text:
                    match = search(r"اتاق\s*:\s*([0-9-]+)", text)
                    if match:
                        return match.group(1)

            return None

        def _email(source: BeautifulSoup):
            email_sibling = source.find(
                "span", {"class": "term"}, text=" پست الکترونیکی "
            )
            if email_sibling:
                email = email_sibling.find_next_sibling("h6", {"class": "description"})
                if email:
                    email_image = email.find("img")
                    if email_image:
                        return email_image.attrs["src"]
            return None

        def _resume(source: BeautifulSoup):
            resume_sibling = source.find("span", {"class": "term"}, text=" رزومه ")
            if resume_sibling:
                resume = resume_sibling.find_next_sibling(
                    "h6", {"class": "description"}
                )
                if resume:
                    resume_link = resume.find("a")
                    if resume_link:
                        return resume_link.attrs["href"]
            return None

        def _scopus(source: BeautifulSoup):
            model = {"Citations": 0, "HIndex": 0, "Until": None}
            scopus_icon = source.find("div", {"class": "sc-icon"})
            if scopus_icon:
                scopus_statistics = scopus_icon.find_next_sibling(
                    "ul", {"class": "content-statistics"}
                )
                citations = (
                    scopus_statistics.find("span", {"class": "label"}, text=" ارجاعات ")
                    .find_previous_sibling("span", {"class": "count increment-counter"})
                    .text
                    if scopus_statistics.find(
                        "span", {"class": "label"}, text=" ارجاعات "
                    )
                    else None
                )
                h_index = (
                    scopus_statistics.find("span", {"class": "label"}, text="h-Index")
                    .find_previous_sibling("span", {"class": "count increment-counter"})
                    .text
                    if scopus_statistics.find(
                        "span", {"class": "label"}, text="h-Index"
                    )
                    else None
                )
                scopus_date = (
                    source.find("div", {"class": "sc-date"})
                    .find("span", {"class": "date-value"})
                    .text
                    if source.find("div", {"class": "sc-date"})
                    else None
                )
                model["Citations"] = int(citations) if citations else None
                model["HIndex"] = int(h_index) if h_index else None
                model["Until"] = (
                    str(helper.persian_to_datetime(scopus_date.strip()))
                    if scopus_date
                    else None
                )
            return model

        def _scholar(source: BeautifulSoup):
            model = {"Citations": 0, "HIndex": 0, "Until": None}
            scholar_icon = source.find("div", {"class": "gsc-icon"})
            if scholar_icon:
                scholar_statistics = scholar_icon.find_next_sibling(
                    "ul", {"class": "content-statistics"}
                )
                citations = (
                    scholar_statistics.find(
                        "span", {"class": "label"}, text=" ارجاعات "
                    )
                    .find_previous_sibling("span", {"class": "count increment-counter"})
                    .text
                )
                h_index = (
                    scholar_statistics.find("span", {"class": "label"}, text="h-Index")
                    .find_previous_sibling("span", {"class": "count increment-counter"})
                    .text
                )
                scholar_date = (
                    source.find("div", {"class": "gsc-date"})
                    .find("span", {"class": "date-value"})
                    .text
                )
                model["Citations"] = int(citations)
                model["HIndex"] = int(h_index)
                model["Until"] = str(helper.persian_to_datetime(scholar_date.strip()))
            return model

        def _graduate(source: BeautifulSoup):
            temp = []
            for case in source.find_all(
                "div",
                {
                    "class": "rendering rendering_personeducation rendering_compact rendering_personeducation_compact"
                },
            ):
                degree = (
                    case.find("p").find("span").text.split(" ،")[0].strip()
                    if case.find("p").find("span")
                    else None
                )
                university_field = (
                    case.find(
                        "span",
                        {
                            "class": "rendering rendering_inline rendering_ueoexternalorganisation rendering_ueoexternalorganisation_inline"
                        },
                    ).text.split("،")
                    if case.find(
                        "span",
                        {
                            "class": "rendering rendering_inline rendering_ueoexternalorganisation rendering_ueoexternalorganisation_inline"
                        },
                    )
                    else None
                )
                start_end = (
                    case.find_all("p")[1].text.split("←")
                    if len(case.find_all("p")) > 1
                    else []
                )
                start_end = start_end if len(start_end) == 2 else ["", ""]
                temp.append(
                    {
                        "Degree": degree,
                        "University": (
                            university_field[0].strip() if university_field else None
                        ),
                        "Field": (
                            university_field[1].strip() if university_field else None
                        ),
                        "Start": int(start_end[0]) if start_end[0].isdigit() else None,
                        "End": int(start_end[1]) if start_end[1].isdigit() else None,
                    }
                )
            return temp

        def _keywords(source: BeautifulSoup):
            section_string = source.find(
                "section",
                {"class": "page-section content-relation-section person-publications"},
            )
            if section_string:
                script_string = section_string.find("script")
                if script_string:
                    string = script_string.text
                    if string:
                        keywords = string[
                            string.find('[{type:"wordcloud",data:')
                            + 24 : string.find(',name:"Occurrences"}]')
                        ]
                        if keywords:
                            return helper.convert_string_to_json(keywords)

            return None

        source = BeautifulSoup(
            get(url=profile_url, headers=self.headers, data=self.payloads).text,
            "html.parser",
        )

        return {
            "Description": _description(source),
            "Major": _major(source),
            "PhoneNumber": _phone_number(source),
            "Room": _room(source),
            "Email": _email(source),
            "Resume": _resume(source),
            "Scopus": _scopus(source),
            "Scholar": _scholar(source),
            "Graduate": _graduate(source),
            "Keywords": _keywords(source),
        }

    def get_profiles(self):

        for end_point in [SearchType.Profile, SearchType.Retired, SearchType.Decedent]:
            url = f"{self.base_url}/{end_point.value}"
            params = self.params.copy()
            params["sortType"] = "last-name"
            params["searchType"] = (
                "dead" if end_point == SearchType.Decedent else end_point.value
            )

            while True:
                page = mongo_tehran.load_page(SearchType.Profile.name, self.use_cache)
                params["page"] = page
                response = get(
                    url=url, params=params, headers=self.headers, data=self.payloads
                )
                if not response.text:
                    break
                if not response.json().get("results", None):
                    mongo_tehran.delete_page(SearchType.Profile.name)
                    break
                else:
                    for result in response.json()["results"]:
                        profile_url = f"{self.base_url}{result.get('url', None)}"
                        profile = {
                            "TeacherId": (
                                int(result.get("teacherId"))
                                if result.get("teacherId")
                                else None
                            ),
                            "Scholarly": [
                                {
                                    "Year": (
                                        int(s.get("year")) if s.get("year") else None
                                    ),
                                    "FirstCount": (
                                        int(s.get("count1"))
                                        if s.get("count1")
                                        else None
                                    ),
                                    "SecondCount": (
                                        int(s.get("count2"))
                                        if s.get("count2")
                                        else None
                                    ),
                                }
                                for s in result.get("scholarly", [])
                            ],
                            "FirstName": result.get("firstName", None),
                            "FirstName_fa_IR": result.get("firstName_fa_IR", None),
                            "FirstName_ar_SA": result.get("firstName_ar_SA", None),
                            "FirstName_en_US": result.get("firstName_en_US", None),
                            "LastName": result.get("lastName", None),
                            "LastName_fa_IR": result.get("lastName_fa_IR", None),
                            "LastName_ar_SA": result.get("lastName_ar_SA", None),
                            "LastName_en_US": result.get("lastName_en_US", None),
                            "Image": f"{self.base_url}{result.get('image', None)}",
                            "Email": result.get("email", None),
                            "EmailBase64": result.get("emailBase64", None),
                            "Url": profile_url,
                            "Degree": result.get("degree", None),
                            "Organistaions": [
                                {"Name": organ.get("name", None)}
                                for organ in result.get("organistaions", [])
                            ],
                        }
                        profile.update(self.complete_profile(profile_url))
                        yield profile
                    mongo_tehran.save_page(SearchType.Profile.name, page + 1)

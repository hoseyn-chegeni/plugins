from re import search, findall, match
from urllib.parse import urlparse, parse_qs


class Helper:

    def find_index(self, string: str, character: str, which: int, reverse: bool = False):
        if reverse:
            string = string[::-1]
            counter = 0
            index = 0
            for x in range(which-1):
                a = string.find(character)
                string = string[:a] + string[a+1:]
                counter += 1
            index = string.find(character) + counter
            return len(string) - index

        else:
            counter = 0
            index = 0
            for x in range(which-1):
                a = string.find(character)
                string = string[:a] + string[a+1:]
                counter += 1
            index = string.find(character) + counter
            return index

    def extract_digits_from_bs4_obj(self, string: str, first_match: bool = True):
        if string:
            matches = findall(r'\d+', string.text)
            if matches:
                if first_match:
                    return int(matches[0])
                else:
                    return [int(match) for match in matches]
            else:
                return 0
        else:
            return 0

    def extract_params_from_url(self, url: str):
        return {key: value[0] for key, value in parse_qs(urlparse(url).query).items()}

    def find_with_regx(self, string: str, pattern: str):
        match = search(pattern, string)
        if match:
            return match.group(1)
        else:
            return None

    def persian_to_datetime(self, persian_date: str):
        m = match(r"^(\d{4})/(\d{2})/(\d{2})$", persian_date)
        if m:
            year, month, day = [int(x) for x in m.groups()]
            return f'{year}-{month}-{day} 00:00:00'
        else:
            return None

    def convert_string_to_json(self, string: str):

        string = string.replace('"', '').replace("'", '').strip()
        elements = string[1:-2].split('},')
        json_objects = []
        
        for element in elements:
            element = element.strip('{}')
            key_values = [item.strip() for item in element.split(',')]
            obj = {}
            for key_value in key_values:
                try:
                    key, value = key_value.split(':')
                    obj[key.strip()] = int(value.strip()) if value.isdigit() else value.strip()
                except ValueError:
                    continue
            
            json_objects.append(obj)
        
        return json_objects

    def remove_nimfasele(self, string: str):
        return string.replace('\u200c', ' ').replace('\xa0', ' ').replace('\u200e', ' ').strip()

    def save_file(self, html: str, filename: str="temp.html"):
        with open(filename, "w", encoding="utf-8") as file:
            file.write(html)

    def persian_to_english_number(self, persian_number: str):
        english_number = persian_number.replace('۰', '0')
        english_number = english_number.replace('۱', '1')
        english_number = english_number.replace('۲', '2')
        english_number = english_number.replace('۳', '3')
        english_number = english_number.replace('۴', '4')
        english_number = english_number.replace('۵', '5')
        english_number = english_number.replace('۶', '6')
        english_number = english_number.replace('۷', '7')
        english_number = english_number.replace('۸', '8')
        return english_number.replace('۹', '9')

    def remove_non_digits(self, input_string: str):
        return ''.join(char for char in input_string if char.isdigit())


helper = Helper()

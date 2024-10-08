from crawlers.universities.base import University
from schemas.employee import Employee

from crawlers.universities.azad.groups.tehran_shargh import (
    get_shimi_prof,
    get_oloom_paye_prof,
    get_zist_prof,
    get_mohandesi_pezeshki_prof,
    get_computer_prof,
    get_omran_prof,
    get_hava_faza_prof,
    get_modiriat_prof,
    get_oloom_ejtemaee_prof,
    get_tarbiat_badain_prof,
    get_hesabdari_prof,
    get_hoquq_prof,
    get_adabiat_prof,
    get_maaref_prof,
    get_honar_prof,
    get_memari_prof,
)


class TehranSharghCrawler(University):
    def __init__(self) -> None:
        self.url = "https://etb.iau.ir/"

    def get_employees(self):
        pass

    def get_colleges(self):
        pass

    def get_professors(self):
        # شیمی
        for professor in get_shimi_prof():
            yield professor
        # علوم پایه
        for professor in get_oloom_paye_prof():
            yield professor
        # زیست
        for professor in get_zist_prof():
            yield professor

        # مهندسی پزشکی
        for professor in get_mohandesi_pezeshki_prof():
            yield professor

        # کامپیوتر
        for professor in get_computer_prof():
            yield professor

        # مهندسی عمران
        for professor in get_omran_prof():
            yield professor

        #  مهندسی مکانیک و مهندسی هوافضا
        for professor in get_hava_faza_prof():
            yield professor

        # مدیریت
        for professor in get_modiriat_prof():
            yield professor

        # علوم اجتماعی
        for professor in get_oloom_ejtemaee_prof():
            yield professor

        # تربیت بدنی
        for professor in get_tarbiat_badain_prof():
            yield professor

        # حسابداری
        for professor in get_hesabdari_prof():
            yield professor

        # حقوق
        for professor in get_hoquq_prof():
            yield professor

        # معارف
        for professor in get_maaref_prof():
            yield professor

        # ادبیات
        for professor in get_adabiat_prof():
            yield professor

        # هنر
        for professor in get_honar_prof():
            yield professor

        # معماری
        for professor in get_memari_prof():
            yield professor

    def get_professor_page(self):
        return super().get_professor_page()

    def get_employee_page(self) -> Employee:
        return super().get_employee_page()

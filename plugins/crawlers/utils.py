from time import sleep

month_persian = {
    "فروردین": 1,
    "اردیبهشت": 2,
    "خرداد": 3,
    "تیر": 4,
    "مرداد": 5,
    "شهریور": 6,
    "مهر": 7,
    "آبان": 8,
    "آذر": 9,
    "دی": 10,
    "بهمن": 11,
    "اسفند": 12
}

def check_connection(func,*args,**kwargs):
    """
    """
    try_connection = 0
    while True:
        try:
            print('Still Crawling')
            response = func(*args,**kwargs)
            sleep(1)
            return response
        except Exception as e:
            print(f"Error in crawler {e}. Sleep for 5 minutes")
            sleep(300)
            try_connection += 1
            if try_connection == 3:
                raise Exception(e)

import datetime
from calendar import HTMLCalendar

class Calendar:
    actuall_day = datetime.date.today().day
    temp_day = 1

    actuall_month = datetime.date.today().month
    temp_month = datetime.date.today().month

    months = [" ","Styczeń","Luty","Marzec","Kwiecień","Maj","Czerwiec","Lipiec","Sierpień","Wrzesień","Październik","Listopad","Grudzień"]
    actuall_month_string = months[actuall_month]
    temp_month_string = months[temp_month]

    actuall_year = datetime.date.today().year
    temp_year = datetime.date.today().year

    def increase_month(self):
        self.temp_month += 1
        if self.temp_month > 12:
            self.temp_month = 1
            self.temp_year += 1

    def decrease_month(self):
        self.temp_month -= 1
        if self.temp_month < 1:
            self.temp_month = 12
            self.temp_year -= 1

cal = Calendar()

import datetime
from calendar import HTMLCalendar

class Calendar:
    actuall_day = datetime.date.today().day
    actuall_month = datetime.date.today().month
    months = [" ","Styczeń","Luty","Marzec","Kwiecień","Maj","Czerwiec","Lipiec","Sierpień","Wrzesień","Październik","Listopad","Grudzień"]
    actuall_month_string = months[actuall_month]
    actuall_year = datetime.date.today().year

    def increase_month(self):
        self.actuall_month += 1

        if self.actuall_month > 12:
            self.actuall_month = 1
            self.actuall_year += 1
            self.actuall_month_string = self.months[self.actuall_month]
        else:
            self.actuall_month_string = self.months[self.actuall_month]

    def decrease_month(self):
        self.actuall_month -= 1

        if self.actuall_month < 1:
            self.actuall_month = 12
            self.actuall_year -= 1
            self.actuall_month_string = self.months[self.actuall_month]
        else:
            self.actuall_month_string = self.months[self.actuall_month]

cal = Calendar()

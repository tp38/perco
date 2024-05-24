import time
import datetime

class Cotation:
    def __init__(self, datev, amount, parts) :
        dd, mm, yyyy = datev.split('/')
        self.date = datetime.date( int(yyyy), int(mm), int(dd) )
        self.amount = float( amount )
        self.set_parts(parts)

    def get_date(self):
        return self.date.strftime("%d/%m/%Y")

    def get_amount(self):
        return self.amount

    def get_parts(self):
        return self.parts

    def get_timestamp(self):
        return time.mktime(datetime.datetime.strptime(self.get_date(), "%d/%m/%Y").timetuple())

    def get_isocalendar(self):
        return self.date.isocalendar()

    def set_parts(self, parts):
        self.parts = float( parts )

    def str(self) :
        return f"{self.date.strftime('%d-%m-%Y')} : {self.amount:.4f} {self.parts:.4f}"

    def xml(self):
        return f"<cotation date='{self.date.strftime('%d-%m-%Y')}' amount='{self.amount}' parts='{self.parts}'></cotation>"

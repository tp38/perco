#!/home/th/Code/Python/Egepargne/bin/python3

import sys
import os
import requests
import csv
import time
import datetime
import matplotlib.pyplot as plt
from datetime import date

from Cotation import Cotation
from Config import DATA_SERVER_STRING


class Fund:
    def __init__(self, name, code, parts ):
        self.name = name
        self.code = code
        self.actual = parts
        self.cotations = []
        self.update = False


    def update_data_file( self, token, verbose ):
        headers = { 'Authorization': f"Bearer {token}", 'Accept': 'text/csv' }
        end = date.today()
        start = f"{end.year - 1}-{end.month:02d}-{end.day:02d}"
        url = DATA_SERVER_STRING.format( fund = self.code, from_date = start, to_date = end )
        try:
            r = requests.get( url, headers=headers )
            r.raise_for_status()
            with open( f"in/{self.name}.csv", 'wb') as f:
                for line in r.iter_lines():
                    f.write( line+'\n'.encode() )
                if verbose :
                    print( f"from {start} to {end} : {self.name}.csv is now up to date" )
        except (requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.RequestException ) :
            if verbose :
                print( f"from {start} to {end} : something goes wrong. {self.name}.csv is unchanged")

    def read_data_from_file(self) :
        parts = {}
        with open( "in/suivi_fonds.csv", "r" ) as fpart:
            rpart = csv.DictReader( fpart, delimiter=";" )
            for lpart in rpart :
                d,m,y = lpart['date'].split('/')
                dpart = f"{d}/{m}/20{y}"
                parts[dpart] = lpart[self.name]

        with open( f"in/{self.name}.csv", 'r') as fquot :
            rquot = csv.DictReader( fquot, delimiter=';' )
            c = None
            for lquot in rquot :
                try :
                    c = Cotation( lquot['date'], lquot['amount'], parts[lquot['date']] )
                except KeyError :
                    c = Cotation( lquot['date'], lquot['amount'], self.actual )
                    self.update = True
                self.cotations.append( c )


    def get_name(self):
        return self.name

    def get_code(self):
        return self.code

    def get_parts(self):
        return self.actual

    def get_update(self):
        return self.update

    def get_date(self):
        return self.cotations[-1].get_date()

    def get_last_stock_market_capital(self):
        c = self.cotations[-1]
        a = c.get_amount()
        p = c.get_parts()
        return a * p

    def get_last_cotation_date(self):
        c = self.cotations[-1]
        return c.get_date()

    def get_last_cotation_parts(self):
        c = self.cotations[-1]
        return c.get_parts()

    def get_last_cotation_value(self):
        c = self.cotations[-1]
        return c.get_amount()

    def get_last_variation(self):
        cn = self.cotations[-1]
        co = self.cotations[-2]
        return cn.get_amount() - co.get_amount()

    def str(self):
        return f"{self.get_name():^10} {self.get_last_cotation_date():>10} " + \
            f"{self.get_last_cotation_parts():>10} {self.get_last_cotation_value():>10.3f} " + \
            f"{self.get_last_variation():>10.3f} {self.get_last_stock_market_capital():>10.3f}"

    def xml(self):
        s = f"<fund name='{self.get_name()}' lcdate='{self.get_last_cotation_date()}' " + \
        f" parts='{self.get_last_cotation_parts():>10.4f}' lcval='{self.get_last_cotation_value():>10.3f}' " + \
        f" lv='{self.get_last_variation():>10.3f}' capital='{self.get_last_stock_market_capital():>10.3f}'>"
        s = s + "</fund>"
        return s

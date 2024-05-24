#!/home/th/Code/Python/Egepargne/bin/python3
import csv
import sys
import subprocess
import matplotlib.pyplot as plt
from paramiko import SSHClient
from scp import SCPClient

from Fund import Fund
from Config import LOGIN, PASWORD, SERVER, S_PATH

class Wallet:
    def __init__(self, file, bearer, verbose ) :
        prop_cycle = plt.rcParams['axes.prop_cycle']
        self.colors = prop_cycle.by_key()['color']
        # self.colors = [ 'blue', 'orange', 'green', 'red', 'violet', 'brown' ]
        self.funds = []
        today_values = ""

        with open( file, 'r') as wf :
            reader = csv.DictReader( wf, delimiter=';' )
            for line in reader :
                f = Fund( line['nom'], line['code'], float(line['parts']) )
                if not bearer == "" :
                    if verbose :
                        print( "trying to update funds data files.")
                    f.update_data_file( bearer, verbose )
                if verbose :
                    print( f"reading data from `{f.get_name()}.csv` file.")
                f.read_data_from_file()
                self.funds.append( f )
                if f.get_update() :
                    if today_values == "" :
                        d,m,Y = f.get_date().split('/')
                        y = int(Y) - 2000
                        today_values = f"{d}/{m}/{y};"
                    else :
                        today_values += ";"
                    today_values += str(f.get_parts())

        print( f"today_values : {today_values}\n" )


    def show_funds_vert(self):
        labels = [ "fond", "nb parts", "date", "valeur", "variation", "capital"]
        print( f"{labels[0]:^10} {labels[2]:^10} {labels[1]:^10} {labels[3]:^10} {labels[4]:^10} {labels[5]:^10}")
        capital = 0.0
        for f in self.funds :
            print( f.str() )
            capital += f.get_last_stock_market_capital()
        #---- le capital total investi
        print( f"=================\n\ttotal : {capital:.2f}\n" )


    def draw_fund_line_chart(self):

        values = []
        i = 0
        fig, ax = plt.subplots()
        for f in self.funds :
            values.append( [] )
            first = True
            ref = 0.0
            for c in f.cotations:
                if first :
                    ref = c.get_amount()
                    first = False
                values[i].append( c.get_amount() - ref )
            ax.plot( values[i], label=f.get_name(), color=self.colors[i] )
            i += 1

        ax.set_ylabel( 'Euros €')
        ax.set_title( f"variations des fonds - 1 an glissant" )
        ax.legend()

        fig.tight_layout()
        # plt.show()
        plt.savefig( "out/01_suivi_fonds.png" )
        plt.close()

    def draw_capital_chart(self):
        values = []
        fig, ax = plt.subplots()
        for f in self.funds :
            j = 0
            for c in f.cotations:
                capital = c.get_amount() * c.get_parts()
                try:
                    values[j] += capital
                except IndexError :
                    values.append( capital )
                j += 1
        ax.plot( values, label="capital" )

        ax.set_ylabel( 'Euros €')
        ax.set_title( f"capital - 1 an glissant" )
        ax.legend()

        fig.tight_layout()
        # plt.show()
        plt.savefig( "out/01_suivi_capital.png" )
        plt.close()

    def draw_fund_evol_chart(self):
        values = []
        i = 0
        fig, axs = plt.subplots(len(self.funds), 1, sharex=True)
        for f in self.funds :
            values.append( [] )
            first = True
            ref = 0.0
            for c in f.cotations:
                parts = c.get_parts()
                if first :
                    ref = parts
                    first = False
                values[i].append( parts )
            axs[i].plot( values[i], label=f.get_name(), color=self.colors[i] )
            axs[i].spines['top'].set_visible(False)
            axs[i].spines['right'].set_visible(False)
            axs[i].spines['bottom'].set_visible(False)
            i += 1
        # ax.set_ylabel( 'Euros €')
        # ax.set_title( f"évolutions des fonds - 1 an glissant" )
        # ax.legend()

        fig.tight_layout()
        # plt.show()
        plt.savefig( "out/01_evol_fonds.png" )
        plt.close()

    def draw_fund_synthese_chart(self):
        values = []
        i = 0
        fig, axs = plt.subplots(len(self.funds), 1, sharex=True)
        for f in self.funds :
            values.append( [] )
            ref_parts = -1.0
            ref_amount = -1.0
            for c in f.cotations:
                parts = c.get_parts()
                amount = c.get_amount()
                if not parts == ref_parts :
                    ref_parts = parts
                    ref_amount = amount
                if amount == ref_amount :
                    values[i].append( 0 )
                elif amount > ref_amount :
                    values[i].append( 5 )
                else :
                    values[i].append( -5 )

            axs[i].plot( values[i], label=f.get_name(), color=self.colors[i] )
            axs[i].spines['top'].set_visible(False)
            axs[i].spines['right'].set_visible(False)
            axs[i].spines['bottom'].set_visible(False)
            i += 1
        # ax.set_ylabel( 'Euros €')
        # ax.set_title( f"évolutions des fonds - 1 an glissant" )
        # ax.legend()

        fig.tight_layout()
        # plt.show()
        plt.savefig( "out/01_synthese_fonds.png" )
        plt.close()

    def xml(self):
        t = ""
        c = 0.0
        for f in self.funds:
            t = t + f.xml() + "\n"
            c += f.get_last_stock_market_capital()
        t = t + "</wallet>"
        s = f"<?xml version='1.0' encoding='UTF-8'?>\n" + \
        f"<?xml-stylesheet type='text/xsl' href='html_report.xsl'?>\n" + \
        f"<wallet capital='{c:10.2f}'>\n"
        return s + t

def scp():
    with SSHClient() as ssh:
        # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.connect("ip", username="username", password="password")
        ssh.load_system_host_keys()
        ssh.connect( SERVER, username = LOGIN, password = PASSWORD )

        with SCPClient(ssh.get_transport()) as scp:
            scp.put('out/report.xml', remote_path=S_PATH)
            scp.put('out/html_report.xsl', remote_path=S_PATH)
            scp.put('out/style.css', remote_path=S_PATH)
            scp.put('out/01_suivi_fonds.png', remote_path=S_PATH)
            scp.put('out/01_suivi_capital.png', remote_path=S_PATH)
            scp.put('out/01_evol_fonds.png', remote_path=S_PATH)
            scp.put('out/01_synthese_fonds.png', remote_path=S_PATH)

def help() :
    print( "usage Wallet.py [option] [bearer=string]" )
    print( "avec option : " )
    print( "\t-f --funds            : visualiser la courbe de suivi des fonds." )
    print( "\t\tdefaut = False" )
    print( "\t-c --capital            : visualiser la courbe de suivi du capital." )
    print( "\t\tdefaut = False" )
    print( "\t-t --transfert-only : uniquement transférer les fichiers vers le serveur web." )
    print( "\t\tne pas se connecter au serveur natixis pour récupérer les données et ne pas" )
    print( "\t\tmettre à jour les fichiers. defaut = False" )
    print( "\t-l --local-only     : ne pas transférer les fichiers vers le serveur web." )
    print( "\t\tuniquement se connecter au serveur natixis, récupérer les données et calculer" )
    print( "\t\tles variations. defaut = False" )
    print( "\t-v --verbose        : mode verbeux" )
    print( "\t-h --help           : cette aide" )


if __name__ == "__main__":
    w = None
    if len(sys.argv) >= 2 :
        argv=sys.argv[1:]
        kwargs={kw[0]:kw[1] for kw in [ar.split('=') for ar in argv if ar.find('=')>0]}
        args=[arg for arg in argv if arg.find('=')<0]

        verbose = False
        funds = False
        capital = False
        transfert_only = False
        local_only = False
        help_screen = False

        for i in range(len(args)):
            if args[i] == "-v" or args[i] == "--verbose" :
                verbose = True
            if args[i] == "-f" or args[i] == "--funds" :
                funds = True
            if args[i] == "-c" or args[i] == "--capital" :
                capital = True
            if args[i] == "-t" or args[i] == "--transfert-only" :
                transfert_only = True
            if args[i] == "-l" or args[i] == "--local-only" :
                local_only = True
            if args[i] == "-h" or args[i] == "--help" :
                help_screen = True

        try:
            bearer = kwargs['bearer']
        except KeyError:
            bearer = ""

        if help_screen :
            help()
        else :
            if not transfert_only :
                w = Wallet( "in/funds.csv", bearer, verbose )
                if verbose :
                    print( "updating charts.")
                w.draw_fund_line_chart()
                w.draw_capital_chart()
                w.draw_fund_evol_chart()
                w.draw_fund_synthese_chart()
                # w.show_funds_vert()
                with open( "out/report.xml", 'w') as f:
                    f.write( w.xml() )

            if funds :
                if verbose :
                    print( "launching image viewer." )
                viewer = subprocess.Popen(['/usr/bin/eog', "out/01_suivi_fonds.png" ])

            if capital :
                if verbose :
                    print( "launching image viewer." )
                viewer = subprocess.Popen(['/usr/bin/eog', "out/01_suivi_capital.png" ])

            if not local_only :
                if verbose :
                    print( "transfering files to web server.")
                scp()
    else :
        print( "launching report viewer." )
        subprocess.Popen(['/usr/bin/epiphany', f"https://{SERVER}/perco/report.xml" ])

#!/home/th/Code/Python/Egepargne/bin/python3
from Wallet import Wallet

if __name__ == "__main__":
    bearer = ""
    verbose = False

    w = Wallet( "in/funds.csv", bearer, verbose )
    w.show_funds_vert()

# PERCO

This code could be used to retreive data concerning PERCO funds from natixis web services and produce charts. This charts are scp to a web server

## Installation

1. Create a virtualenv in ~/perco (or wherever you want) with :
    > $ virtualenv ~/perco
2. Just download this project on local (ie : ~/perco/prod/ ).
3. Activate the virtual env with 
    > $ source ~/perco/bin/activate
4. Install required modules with :
    > (perco)$ pip install --upgrade pip
    > (perco)$ pip install -r requirements.txt
    > (perco)$ deactivate
5. Copy the Config.py.example in Config.py 
    > cp Config.py.example Config.py


## Configuration

There's tree files (**in/funds.csv**, **in/suivi_fonds.csv** and **Config.py**) to configure. 

### funds.csv

In this file, we must indicate which funds we'd like to retrieve and analyze.

The format is 1st line for headers and next lines for funds definition.
Each fund must containt this fields :
1. fund's name
2. fund's code (issuing from natixis system)
3. fund's actual nb parts

### suivi_fonds.csv

In this file, we must save day by days the number of parts for each funds (to create charts). The format is 1st line for headers (date and fund's name) and next lines for each days.
Each day must containt this fields :
1. date
2. to n. : corresponding fund nb parts

### Config.py

In this file, we must setup some parameters :
- SERVER : the server where we upload output files (out/*)
- S_PATH : the path on SERVER where to upload files (LOGIN/PASSWORD must have write access on this directory)
- LOGIN : the account use to upload files
- PASSWORD : the password use to upload
- DATA_SERVER_STRING : the URL use to download funds data files. This string must contain three parameterized fields named {fund} for fund code, {from} for start date and {to} for end date (see python string format for more explaination ) 


## Usage

This is a three stage process :
1. check if funds.csv ans suivi_fonds.csv are up to date with this two command line :
    > $ cat in/funds.csv
    > $ tail -1 in/*suivi_fonds.csv
2. retreive bearer (bearer_string) from natixis auth
3. launch ./Wallet.py like above

```
    usage Wallet.py [option] [bearer=string]
    with option :

    -f|--funds          : only display funds charts (defaut = False).    
    -c|--capital        : only display capital chart (defaut = False).    
    -t|--transfert-only : only transfert files to web server.   
                do not connect to bank server to retreive data and do not update files and charts (defaut = False).    
    -l|--local-only     : do not transfer files to web server. Just connect to bank server,
                retreive data and update charts files (defaut = False)    
    -v|--verbose        : verbose mode    
    -h|--help           : this help
```

## Results

to consult results :  http://server_web/perco/report.xml
import getopt
import os
import sys

import requests


ftp_username = os.environ.get('FTP_USERNAME','')
ftp_password = os.environ.get('FTP_PASSWORD','')
ftp_hostname = os.environ.get('FTP_HOSTNAME','')
netstorage_path = os.environ.get('NETSTORAGE_PATH','')

api_name = None
host = None
country_code = None

headers = {
    'authority':'webx.hotstar.com',
    'accept':'application/json, text/plain, */*',
    'accept-language':'eng',
    'cache-control':'no-cache',
    'hotstarauth':'st=1668236089~exp=1668242089~acl=/*~hmac=ff38e75337d7970078b99ac1a1b4d60562ed5b1265cc77b880b2b9e27450da0f',
    'pragma':'no-cache',
    'referer':'https://webx.hotstar.com/ph/home',
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'x-country-code':'ph',
    'x-hs-accept-language':'eng',
    'x-hs-platform':'web'
}



argumentList = sys.argv[1:]
 
# Options
#TODO add optional parmaters for query params
options = "a:h:c:q"


 
# Long options
long_options = ["API", "Host", "Country_code"]
 
try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)
     
    # checking each argument
    for currentArgument, currentValue in arguments:
 
        if currentArgument in ("-a", "--API"):
            api_name = currentValue
            print ("API " , currentValue)
             
        elif currentArgument in ("-h", "--Host"):
            host = currentValue
            print ("Host = ", currentValue)
        
        elif currentArgument in ("-c", "--Country_code"):
            country_code = currentValue
            print("Country code = ", country_code)

        
             
             
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))

request_url = host+api_name
response = requests.get(request_url, headers=headers)
print(response)


#connect to NS to store the file
#Net storage is from env variable + folder name from api name & country code
        

      
    








import getopt
import os
import sys

import requests


akamai_netstorage_ftp_username = os.environ.get('AKAMAI_NETSTORAGE_FTP_USERNAME','') 
akamai_netstorage_ftp_password = os.environ.get('AKAMAI_NETSTORAGE_FTP_PASSWORD','')
akamai_netstorage_ftp_hostname = os.environ.get('AKAMAI_NETSTORAGE_FTP_HOSTNAME','') 
akamai_netstorage_ftp_path = os.environ.get('AKAMAI_NETSTORAGE_PATH','') 



request_path = None #rp 
cluster = None # c 
request_type = None # t
file_storage_path = None #fp
data = None
headers = None 
query_params = None


argumentList = sys.argv[1:]
 
options = "r:c:t:f:"
long_options = ["RequestPath", "Cluster", "RequestType", "FileStoragePath"]
 
try:
    arguments, values = getopt.getopt(argumentList, options, long_options)
     
    for currentArgument, currentValue in arguments:
 
        if currentArgument in ("-r", "--RequestPath"):
            request_path = currentValue
            print ("RequestPath " , currentValue)
             
        elif currentArgument in ("-c", "--Cluster"):
            cluster = currentValue
            print ("Host = ", currentValue)
        
        elif currentArgument in ("-t", "--RequestType"):
            request_type = currentValue
            print("Request Type = ", request_type)
        
        elif currentArgument in ("-f", "--FileStoragePath"):
            file_storage_path = currentValue
            print("FileStoragePath = ", file_storage_path)

except getopt.error as err:
    print (str(err))


response = requests.get(request_path, headers=headers)
print(response)

        

      
    






#curl -v 'https://webx.hotstar.com/api/internal/bff/v2/slug/ph/paywall'   -H 'authority: webx.hotstar.com'   -H 'accept: application/json, text/plain, */*'   -H 'accept-language: eng'   -H 'cache-control: no-cache'   -H 'hotstarauth: st=1668236089~exp=1668242089~acl=/*~hmac=ff38e75337d7970078b99ac1a1b4d60562ed5b1265cc77b880b2b9e27450da0f'   -H 'pragma: no-cache'   -H 'referer: https://webx.hotstar.com/ph/home'   -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'   -H 'x-country-code: ph'   -H 'x-hs-accept-language: eng'   -H 'x-hs-platform: web'

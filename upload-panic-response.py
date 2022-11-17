import getopt
import os
import sys
import pandas as pd
import requests
import re
from dotenv import dotenv_values



environment_name = None #e
request_path = None #r
cluster = None # c 
request_type = None # t
file_storage_path = None #f
header_file_location = None #h
data = None
headers = None 
query_params = None

argumentList = sys.argv[1:]
 
options = "e:r:c:t:f:h:"
long_options = ["EnviornmentName", "RequestPath", "Cluster", "RequestType", "FileStoragePath", "HeaderFileLocation"]
 
try:
    arguments, values = getopt.getopt(argumentList, options, long_options)
     
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-e", "--EnviornmentName"):
            environment_name = currentValue
            print ("EnviornmentName " , currentValue)
 
        elif currentArgument in ("-r", "--RequestPath"):
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
        
        elif currentArgument in ("-h", "--HeaderFileLocation"):
            header_file_location = currentValue
            print("HeaderFileLocation = ",header_file_location)


except getopt.error as err:
    print (str(err))

config_file_name = ".env."+environment_name
config = dotenv_values(config_file_name)
akamai_netstorage_ftp_username = config.get('AKAMAI_NETSTORAGE_FTP_USERNAME') 
akamai_netstorage_ftp_password = config.get('AKAMAI_NETSTORAGE_FTP_PASSWORD')
akamai_netstorage_ftp_hostname = config.get('AKAMAI_NETSTORAGE_FTP_HOSTNAME') 
akamai_netstorage_ftp_path = config.get('AKAMAI_NETSTORAGE_PATH','') 


#reading headers
headers_file_content = requests.get(header_file_location)
headers_text = headers_file_content.text.strip()

header_json = re.search(r'\{(.|\s)*\}',  headers_text)
header_json = header_json.group(0).replace('false', 'False')
headers = eval(header_json)

print("\n",headers, "\n") 

if request_type in ("get", "GET", "Get"):
    response = requests.get(request_path, headers=headers)
elif request_type in ("post", "POST", "Post"):
    response = requests.post(request_path, headers=headers)
else:
    print("Only GET and POST are supported request types")
    
print("\n", response, "\n")

        

      
    








import getopt
import os
import sys
import pandas as pd
import requests
import re
from dotenv import dotenv_values
from ftplib import FTP, FTP_TLS
import configparser

environment_name = None 


argumentList = sys.argv[1:]
 
options = "e:"
long_options = ["EnviornmentName"]
try:
    arguments, values = getopt.getopt(argumentList, options, long_options)
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-e", "--EnviornmentName"): #continue from cmd line
            environment_name = currentValue
except getopt.error as err:
    print (str(err))

#fetching values from config file wrt to env 

config = dotenv_values(".env")
akamai_netstorage_ftp_username = config.get('AKAMAI_NETSTORAGE_FTP_USERNAME') 
akamai_netstorage_ftp_password = config.get('AKAMAI_NETSTORAGE_FTP_PASSWORD')
akamai_netstorage_ftp_hostname = config.get('AKAMAI_NETSTORAGE_FTP_HOSTNAME') 
akamai_netstorage_folder_path = config.get('AKAMAI_NETSTORAGE_FOLDER_PATH')


#fetching environment specific inputs
config_file_name = "./config/.env."+environment_name
environment_config = dotenv_values(config_file_name)
cluster = environment_config.get('CLUSTER')
request_url = environment_config.get('REQUEST_URL')
header_file_location = environment_config.get('HEADER_FILE_PATH')
request_type = environment_config.get('REQUEST_TYPE')



#connect to akamai netstorage
ftp = FTP_TLS(akamai_netstorage_ftp_hostname)
usercmd = 'USER '+str(akamai_netstorage_ftp_username)
ftp.sendcmd(usercmd)
passcmd = 'PASS '+str(akamai_netstorage_ftp_password)
ftp.sendcmd(passcmd)
ftp.cwd(akamai_netstorage_folder_path)
list = ftp.nlst()
print(list)
ftp.quit()


#reading headers
header_file = open(header_file_location)
headers = header_file.read()
header_file.close()



# print("\n",headers, "\n") 

response = None
if request_type in ("get", "GET", "Get"):
    response = requests.get(request_url, headers=headers)
elif request_type in ("post", "POST", "Post"):
    response = requests.post(request_url, headers=headers)
else:
    print("Error : Only GET and POST are supported request types")
    
# print("\n", response, "\n")



###########

        

      
    








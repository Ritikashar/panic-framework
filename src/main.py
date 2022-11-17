import getopt
import os
import sys
import pandas as pd
import requests
import re
from dotenv import dotenv_values
from ftplib import FTP, FTP_TLS
import configparser

def main():
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

    akamai_config = get_akamai_config() 
    environment_config = get_environment_config(environment_name)
    panic_response = create_panic_response_file(akamai_config,environment_config)
    upload_panic_response(panic_response,akamai_config,environment_config)

if __name__ == "__main__":
    main()

def get_akamai_config():
    akamai_config = dotenv_values(".env")
    akamai_config = {
        "akamai_netstorage_ftp_username" : config.get('AKAMAI_NETSTORAGE_FTP_USERNAME') ,
        "akamai_netstorage_ftp_password" : config.get('AKAMAI_NETSTORAGE_FTP_PASSWORD'),
        "akamai_netstorage_ftp_hostname" :  config.get('AKAMAI_NETSTORAGE_FTP_HOSTNAME') ,
        "akamai_netstorage_folder_path" : config.get('AKAMAI_NETSTORAGE_FOLDER_PATH'),
    }
    
    return akamai_config

def get_environment_config(environment_name):
    config_file_name = "./config/.env."+environment_name
    environment_config = dotenv_values(config_file_name)
    return {
        "cluster":environment_config.get('CLUSTER'),
        "request_url":environment_config.get('REQUEST_URL'),
        "header_file_location":environment_config.get('HEADER_FILE_PATH'),
        "request_type":environment_config.get('REQUEST_TYPE')
    }

def get_headers(header_file_location):
    header_file = open(header_file_location)
    headers = header_file.read()
    header_file.close()
    return headers

def create_panic_response_file(akamai_config, environment_config):
    response = None
    request_type = environment_config.get("REQUEST_TYPE", None)
    request_url = environment_config.get("REQUEST_URL", None)
    headers = get_headers(environment_config.get("HEADER_FILE_PATH", None))
    if request_type in ("get", "GET", "Get"):
        response = requests.get(request_url, headers=headers)
    elif request_type in ("post", "POST", "Post"):
        response = requests.post(request_url, headers=headers)
    else:
        print("Error : Only GET and POST are supported request types")
        
    print("\n", response, "\n")
    return None

def upload_panic_response(panic_response,akamai_config,environment_config):
    #connect to akamai netstorage
    ftp = FTP_TLS(akamai_config.get("akamai_netstorage_ftp_username", None))
    usercmd = 'USER '+str(akamai_config.get("akamai_netstorage_ftp_username",None))
    ftp.sendcmd(usercmd)
    passcmd = 'PASS '+str(akamai_config.get("akamai_netstorage_ftp_password", None))
    ftp.sendcmd(passcmd)
    ftp.cwd(akamai_config.get("akamai_netstorage_folder_path",None))
    list = ftp.nlst()
    #create file
    print(list)
    ftp.quit()
      
    








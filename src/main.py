import getopt
import os
import sys
import pandas as pd
import requests
import re
from dotenv import dotenv_values
from ftplib import FTP, FTP_TLS
import configparser
import json
import http


TEMP_RESPONSE_BODY_FILE_PATH = "./temp_response_body"

def get_akamai_config():
    akamai_config = dotenv_values(".env")
    return {
        "akamai_netstorage_ftp_username": akamai_config.get('AKAMAI_NETSTORAGE_FTP_USERNAME'),
        "akamai_netstorage_ftp_password": akamai_config.get('AKAMAI_NETSTORAGE_FTP_PASSWORD'),
        "akamai_netstorage_ftp_hostname": akamai_config.get('AKAMAI_NETSTORAGE_FTP_HOSTNAME'),
        "akamai_netstorage_folder_path": akamai_config.get('AKAMAI_NETSTORAGE_FOLDER_PATH'),
    }

    return akamai_config


def get_environment_config(config_file_name):
    environment_config = dotenv_values(config_file_name)

    return {
        "request_url": environment_config.get('REQUEST_URL'),
        "header_file_location": environment_config.get('HEADER_FILE_PATH'),
        "request_type": environment_config.get('REQUEST_TYPE'),
        "header_file_location": environment_config.get('HEADER_FILE_LOCATION'),
        "data_file_location": environment_config.get('DATA_FILE_LOACTION'),
    }


def get_headers(header_file_location):
    if header_file_location == "":
        return {}

    headers = {}
    try:
        with open(header_file_location) as myfile:
            for line in myfile:
                k, v = line.partition(":")[::2]
                headers[k.strip()] = v.strip()
            myfile.close()
            return headers  
    except Exception as e:
        print("Exception in get_headers : ", e.__class__, "occurred.\n")
        sys.exit()
    


def get_body(data_file_location):
    if data_file_location == "":
        return ""
    data_file = open(data_file_location)
    data = data_file.read()
    data_file.close()
    return data


def get_panic_response(configurations, user_inputs):
    headers = get_headers(user_inputs["request_header_file_location"])
    body = get_body(user_inputs["request_body_file_location"])
    req_path = configurations["cluster"][user_inputs["pcomp_env"]
                                         ]["pcomp_endpoint"]+user_inputs["request_path"]
    req_method = user_inputs["request_method"]

    # req = requests.Request(req_method, req_path, headers=headers, data=body).prepare()

    response = None
    if req_method in ("get", "GET", "Get"):
        response = requests.get(req_path, headers=headers, data=body)
    elif req_method in ("post", "POST", "Post"):
        response = requests.post(req_path, headers=headers, data=body)
    else:
        print("Not valid method : ", req_method)
        sys.exit()

    print("Response status: ", response.status_code, "\n")
    print("Response headers : ", response.headers, "\n")
    print("Response body:", response.content, "\n")
    response.status_code = 200
    
    if response.status_code != 200:
        print("Non 200 response status, exiting...")
        sys.exit()

    if os.path.exists(TEMP_RESPONSE_BODY_FILE_PATH):
        os.remove(TEMP_RESPONSE_BODY_FILE_PATH)
    
    f = open(TEMP_RESPONSE_BODY_FILE_PATH, "x")
    f.write(response.content.decode())
    f.close()


def upload_panic_response(configurations, user_inputs):
    ns_hostname = configurations["akamai"]["ns_hostname"]
    ns_username = os.environ["AKAMAI_NS_USERNAME"]
    ns_password = os.environ["AKAMAI_NS_PASSWORD"]

    ftp = FTP_TLS(ns_hostname)
    usercmd = 'USER ' + ns_username
    ftp.sendcmd(usercmd)
    passcmd = 'PASS ' + ns_password
    ftp.sendcmd(passcmd)
    
    ns_prefix = configurations["cluster"][user_inputs["pcomp_env"]]["ns_prefix"]
    ns_path =  os.path.join(configurations["akamai"]["ns_prefix_path"], ns_prefix , user_inputs["ns_file_path_suffix"])
    dir_path = ""
   
    for i in ns_path.rsplit('/', 1)[0].split('/'):
        dir_path = os.path.join(dir_path,i)
        if i not in ftp.nlst(os.path.dirname(dir_path)):
            ftp.mkd(dir_path)

    file = open(TEMP_RESPONSE_BODY_FILE_PATH,'rb')                  
    ftp.storbinary(ns_path, file)
    file.close()
    ftp.quit()


def get_json_data(config_file):

    try:
        json_file = open(config_file)
        json_str = json_file.read()
        json1_data = json.loads(json_str)
        return json1_data

    except Exception as e:
        print("Exception : ", e.__class__, "occurred.\n")
        sys.exit()


def read_user_inputs(configurations):

    user_input = {
        "request_path": os.environ['REQUEST_PATH'],
        "request_method": os.environ['REQUEST_METHOD'],
        "request_header_file_location": os.environ['REQUEST_HEADER_FILE_LOCATION'],
        "request_body_file_location": os.environ['REQUEST_BODY_FILE_LOACTION'],
        "ns_file_path_suffix" : os.environ['AKAMAI_NS_FILE_PATH_SUFFIX'],
        "pcomp_env": os.environ['PCOMP_ENV']
    }

    if user_input["pcomp_env"] not in configurations["cluster"]:
        print("Invalid value for : PCOMP_ENV")
        sys.exit()

    return user_input


def main():
    try:
        environment_name = None
        argumentList = sys.argv[1:]
        options = "e:"
        long_options = ["env"]

        
        arguments, values = getopt.getopt(argumentList, options, long_options)
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-e", "--env"):
                environment_name = currentValue


        config_file = "./config/nonprod.json"
        if environment_name == 'prod' or environment_name == 'PROD':
            config_file = "./config/prod.json"

        configurations = get_json_data(config_file)
        user_inputs = read_user_inputs(configurations)
        get_panic_response(configurations, user_inputs)
        upload_panic_response(configurations, user_inputs)

    except Exception as e:
        print("Exception : ", e.__class__, "occurred.\n")
        sys.exit()



if __name__ == "__main__":
    main()

# read csv 
import csv
from dbm.ndbm import library
import os
import sys
import json
import pandas as pd
import json, requests, urllib, io
# For args
import argparse
from urllib.request import urlopen


# taking command line input 
msg="Welcome to the Dyte CLI . Your reliable dependabot clone without the annoying Notifications :) ";
parser = argparse.ArgumentParser(description=msg)
parser.add_argument('-u' , '--update' , help="Update the Dependancy CLI"  , nargs='?' )
parser.add_argument('-i', '--input', help='File to be read', nargs='+' , required=True)
args = parser.parse_args()

def getNodeModulesFile(url):
    # github username from env FIle
     url+="/blob/main/package.json"
     github_session = requests.Session();
     modifiedURL = url.replace('github.com', 'raw.githubusercontent.com');
     modifiedURL = modifiedURL.replace('/blob/', '/');
     # download file with curl and save it 
     response = urlopen(modifiedURL)
     data_json = json.loads(response.read())
     return data_json

dependencies = getNodeModulesFile("https://github.com/dyte-in/react-sample-app")['dependencies'];

librariesList = []

for _, value in parser.parse_args()._get_kwargs():
    if value is not None:
        print(value)
        librariesList = value[1:]
#Check Whether required Libraries are present in the list
libraryDictionary={}
for library in librariesList:
    #split string at @ symbol as name and val
    libraryName = library.split('@')[0]
    libraryVersion = library.split('@')[1]
    libraryDictionary[libraryName] = libraryVersion
print(libraryDictionary);

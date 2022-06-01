from cProfile import run
import csv
from dbm.ndbm import library
from doctest import REPORT_CDIFF
import json, requests
from sys import stdout
from pip import main
from pickle import FALSE
import os 
import argparse
from urllib.request import urlopen
import subprocess
from dotenv import load_dotenv
from github import Github
from base64 import b64encode
from json import dumps
from tabulate import tabulate

load_dotenv();

g = Github(os.getenv('GITHUB_AUTH_TOKEN'));
username = os.getenv('GITHUB_USERNAME');
auth_token = os.getenv('GITHUB_AUTH_TOKEN');

#Superss Output of runcmd
# taking command line input 
msg="Welcome to the Dyte Dependency CLI . Your reliable dependabot clone without the annoying Notifications :) ";
parser = argparse.ArgumentParser(description=msg)
parser.add_argument('-u' , '--update' , help="Update the Dependancy CLI"  , nargs='?' )
parser.add_argument('-i', '--input', help='File to be read', nargs='+' , required=True)
args = parser.parse_args()


librariesList = []
for _, value in parser.parse_args()._get_kwargs():
    if value is not None:
        librariesList = value[1:]
#Check Whether required Libraries are present in the list
inputDict={}
for library in librariesList:
    #split string at @ symbol as name and val
    libraryName = library.split('@')[0]
    libraryVersion = library.split('@')[1]
    inputDict[libraryName] = libraryVersion

#reading dataset.csv
links=[]

with open('Dataset.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile , delimiter=',')
    i=1
    for row in csvreader:
        links.append(row[1])
links=links[1:]
def convertBase64ToJson(base64):
    return json.loads(base64)
def getPackageJson(link):
    name = link.split('/')[-1];
    repo = g.get_repo(username + "/" + name);
    pjson = repo.get_contents("package.json")
    # get base64 encoded content
    base64 = pjson.decoded_content
    # convert base64 to json
    json_data = convertBase64ToJson(base64)
    return json_data  

# create table to store name and required version of each library
print("Given Dependency Lists")
def createTable(inputDict):
    table = []
    for key, value in inputDict.items():
        table.append([key, value])
    return table

print(tabulate(createTable(inputDict), headers=['Library', 'Required Version']))
table = []


def getRepositoryName(link):
    name = link.split('/')[-1]
    return name 
for link in links:
    deps = getPackageJson(link)['dependencies']    
    #iterate over given libraries to find if deps are present
    for library in inputDict:
        if library in deps:
            #remove first char from deps[library]
            if inputDict[library] == deps[library].split('^')[1]:
                #Add to table saying Curr Version is same as Required Version
                table.append([library, inputDict[library] , deps[library].split('^')[1]])
            else:
                #Add to table saying Curr Version is not same as Required Version
                table.append([library,inputDict[library] ,  deps[library].split('^')[1]])
        else:
            #Add to table saying Library is not present in the Repository
            table.append([library, "Not Present"])
    print("For Repository Name " + getRepositoryName(link))
    print(tabulate(table, headers=['Library', 'Required Version', 'Current Version']))
    #Clear Table for next Repository
    table = []
    print("\n")

#get repo name from link
def getCompanyName(link):
    name = link.split('/')[-2];
    return name
table = []
# Table to store Repo Name Library Version Needed Version and Pull Request URL
if args.update:
    for link in links:
        #Fork Using pygithub
        organisation_name = getCompanyName(link);
        repo = g.get_repo(organisation_name + "/" + getRepositoryName(link))
        repo.create_fork()
        name = getRepositoryName(link)
        #Get Forked Repo
        forked_repo = g.get_repo(username + "/" + getRepositoryName(link))
        fored_repo_link = forked_repo.html_url
        jsonData = getPackageJson(fored_repo_link);
        packjson = forked_repo.get_contents("package.json")
        for library in inputDict:
            if library in jsonData['dependencies']:
                #remove first char from deps[library]
                jsonData['dependencies'][library] = "^"+inputDict[library]
        #write the changes to the file
        print(jsonData)
        #commit the changes
        forked_repo.update_file("package.json", "Updating Dependencies", json.dumps(jsonData), packjson.sha, branch="main")
        #Open Pull Request 
        #pr = forked_repo.create_pull(title="Update Dependencies", body="Update Dependencies", head="main", base="main")
        #get Pull Request URL
        #pull_request_url = repo.get_pulls()[0].html_url
        #Add to table 
        #table.append([name, library, inputDict[library], pull_request_url])
    print(tabulate(table, headers=['Repository Name', 'Library', 'Required Version', 'Pull Request URL']))
    #clear table
    table = []

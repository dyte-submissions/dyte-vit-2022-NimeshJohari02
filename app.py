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


def runcmd(cmd, verbose = FALSE, *args, **kwargs):
    process = subprocess.Popen(
        cmd +" > /dev/null",
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True,
        shell = True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)
    pass
#Superss Output of runcmd
# taking command line input 
msg="Welcome to the Dyte Dependency CLI . Your reliable dependabot clone without the annoying Notifications :) ";
parser = argparse.ArgumentParser(description=msg)
parser.add_argument('-u' , '--update' , help="Update the Dependancy CLI"  , nargs='?' )
parser.add_argument('-i', '--input', help='File to be read', nargs='+' , required=True)
args = parser.parse_args()

def getRawURL(url):
    url+="/blob/main/package.json"
    modifiedURL = url.replace('github.com', 'raw.githubusercontent.com');
    modifiedURL = modifiedURL.replace('/blob/', '/');
    return modifiedURL
         
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
def matchString(s1 , s2):
    if s1 in s2:
        return True
    else:
        return False

with open('Dataset.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile , delimiter=',')
    i=1
    for row in csvreader:
        links.append(row[1])
links=links[1:]
# create a dictionary of links and their unmet dependencies
# I need a datastructure that would allow me to store the unmet dependencies for each link
# i need to create a dictionary with the links as keys and the dependencies as values
def downloadFile(link):      
    name = link.split('/')[-1];
    cmd = "curl " + getRawURL(link)+" --create-dirs -o jsonFiles/"+name+"/package.json"
    createDirs = runcmd(cmd , verbose=FALSE);

def convertBase64ToJson(base64):
    return json.loads(base64)

# This function is to get packagejson for private repositories 

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
    try:
        deps = getNodeModulesFile(link)['dependencies']
    except:
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
def performShallowClone(link):
    name = link.split('/')[-1];
    #get repo name from link
    cmd = "git clone " + link + " --depth 1 --branch main --single-branch jsonFiles/"+name
    # pipe output of command to null
    clone = runcmd(cmd , verbose=FALSE );
def clonePrivateRepo(link):
    name = link.split('/')[-1];
    cmd ="gh repo clone "+username+":"+name +" jsonFiles/"+name
    clonePvt = runcmd(cmd , verbose=FALSE);
# def getPackageJSON(link):
#     name = getRepositoryName(link);
#     repository =g.get_repo(os.getenv('GITHUB_USERNAME')+'/'+name)
#     content = repository.get_contents('package.json')
#     base64_string = content.decode('utf-8')
#     json_data = dumps(base64_string, indent=2)
#     return json_data

def getForkURLFromURL(link):
    name = link.split('/')[-1];
    modifiedLink = "https://github.com/"+os.getenv('GITHUB_USERNAME')+"/"+name;
    return modifiedLink

def getCompanyName(link):
    name = link.split('/')[-2];
    return name
table = []
# Table to store Repo Name Library Version Needed Version and Pull Request URL
if args.update:
    #fork the repo 
    for link in links:
        cmd ="gh repo fork "+link;
        forkRepo = runcmd(cmd , verbose=FALSE);
        #get fork url
        name = getRepositoryName(link);
        str = getForkURLFromURL(link);
        try:
            performShallowClone(str)
        except:
            clonePrivateRepo(str)
        #open the package.json file
        with open('jsonFiles/'+name+'/package.json', 'r') as f:
            data = json.load(f)
        #iterate over the inputDict
        for library in inputDict:
            if library in data['dependencies']:
                #remove first char from deps[library]
                data['dependencies'][library] = "^"+inputDict[library]
        #write the changes to the file
        with open('jsonFiles/'+name+'/package.json', 'w') as f:
            json.dump(data, f)
        #commit the changes to another branch
        #generate name for branch
        branchName = "update_"+library+"_"+inputDict[library]
        cmd = "cd jsonFiles/"+name+" && git checkout -b" +branchName+"&&  git add package.json && git commit -m 'updated dependencies' && git push --force origin "+branchName
        commitChanges = runcmd(cmd , verbose=FALSE);
        #open pull request using pygithub
        organisation_name = getCompanyName(link);
        #repo = g.get_repo(username+'/'+name)
        #create a pull request using pygithub
        try:
            #create pr from deps to master
           # cmd="""curl -u """+ username+""":"""+auth_token+""" -X POST -H "Accept: application/vnd.github.v3+json"  https://api.github.com/repos/"""+organisation_name+"/"+name+"""/pulls -d '{"title":"Update Dependency ","body":"Update Dependencies","head":"""+'"'+username+":"+branchName+'"'+""","base":"main"}'""";
            #createPr = runcmd(cmd , verbose=False)
            #get the pull request url and store in variable
            cmd = "curl -u "+username+":"+auth_token+" -X GET -H \"Accept: application/vnd.github.v3+json\" https://api.github.com/repos/"+organisation_name+"/"+name+"/pulls"
            #get Last Request from cmd 
            pullRequestURL = runcmd(cmd , verbose=FALSE);
            table.append([name, library, inputDict[library], deps[library].split('^')[1], pullRequestURL]);
        except Exception as e:
            print(e);
        #pr ="""gh api --method POST -H "Accept: application/vnd.github.v3+json" /repos/{}/{}/pulls -f title='Dependency Update' -f body='Please pull these awesome changes in!' -f head='{}:{}' -f base={}""".format(organisation_name,name,username,name,'main');
        # runcmd(pr , verbose=FALSE);
        #delete from local Storage
        cmd = "rm -rf jsonFiles/"+name
        remove = runcmd(cmd , verbose=FALSE);
        # Check For Already Made PR 
        #Create Table
        print(tabulate(table, headers=['Repository Name', 'Library', 'Required Version', 'Current Version', 'Pull Request URL']))
        table=[];

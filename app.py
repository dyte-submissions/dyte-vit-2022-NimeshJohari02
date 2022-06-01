from cProfile import run
import csv
from dbm.ndbm import library
from doctest import REPORT_CDIFF
import json, requests
from pip import main
from pickle import TRUE
import os 
import argparse
from urllib.request import urlopen
import subprocess
from dotenv import load_dotenv
from github import Github
from base64 import b64encode
from json import dumps


load_dotenv();
g = Github(os.getenv('GITHUB_AUTH_TOKEN'));
username = os.getenv('GITHUB_USERNAME');


def runcmd(cmd, verbose = False, *args, **kwargs):
    process = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True,
        shell = True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)
    pass

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
        print(value)
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
    print(link)
    print(name)
    print(getRawURL(link))
    cmd = "curl " + getRawURL(link)+" --create-dirs -o jsonFiles/"+name+"/package.json"
    runcmd(cmd , verbose=TRUE);

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

for link in links:
    print("For Repository with the Link " + link)
    try:
        deps = getNodeModulesFile(link)['dependencies']
    except:
        deps = getPackageJson(link)['dependencies']    
    #iterate over given libraries to find if deps are present
    for library in inputDict:
        if library in deps:
            #remove first char from deps[library]
            if inputDict[library] == deps[library].split('^')[1]:
                print(library + " is present in the Repository and version Match "  )
            else:
                print( library + " Existing Version" + deps[library] + "Needed Version" + inputDict[library])

        else:
            print("Library " + library + " is not present in the Repository " + link)
    print("\n")


def getRepositoryName(link):
    name = link.split('/')[-1]
    return name 

#get repo name from link
def performShallowClone(link):
    name = link.split('/')[-1];
    #get repo name from link
    cmd = "git clone " + link + " --depth 1 --branch main --single-branch jsonFiles/"+name
    runcmd(cmd , verbose=TRUE);

# def getPackageJSON(link):
#     name = getRepositoryName(link);
#     repository =g.get_repo(os.getenv('GITHUB_USERNAME')+'/'+name)
#     content = repository.get_contents('package.json')
#     print(content);
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

if args.update:
    print("Updating Dependencies");
    #fork the repo 
    for link in links:
        cmd ="gh repo fork "+link;
        runcmd(cmd , verbose=TRUE);
        #get fork url
        name = getRepositoryName(link);
        str = getForkURLFromURL(link);
        performShallowClone(str)
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
        #commit the changes
        cmd = "cd jsonFiles/"+name+" && git add package.json && git commit -m 'updated dependencies' && git push origin main"
        runcmd(cmd , verbose=TRUE);
        #open pull request using pygithub
        organisation_name = getCompanyName(link);
        repo = g.get_repo(username+'/'+name)
        #create a pull request using pygithub
        try:
            pr = repo.create_pull(title="Update Dependencies", body="Update Dependencies", head=organisation_name+':main', base='main')
        # catch 
        except Exception as e:
            print(e);
            print("Pull Request Already Exists")
        #pr ="""gh api --method POST -H "Accept: application/vnd.github.v3+json" /repos/{}/{}/pulls -f title='Dependency Update' -f body='Please pull these awesome changes in!' -f head='{}:{}' -f base={}""".format(organisation_name,name,username,name,'main');
        # runcmd(pr , verbose=TRUE);
        #delete from local Storage
        cmd = "rm -rf jsonFiles/"+name
        runcmd(cmd , verbose=TRUE);
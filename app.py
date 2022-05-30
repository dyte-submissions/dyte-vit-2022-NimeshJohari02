import csv
from dbm.ndbm import library
import json
import json, requests 
# For args
import argparse
from urllib.request import urlopen


# taking command line input 
msg="Welcome to the Dyte Dependency CLI . Your reliable dependabot clone without the annoying Notifications :) ";
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

#dependencies = getNodeModulesFile("https://github.com/dyte-in/react-sample-app")['dependencies'];

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
#iterate over the links 
for link in links:
    print("For Repository with the Link " + link)
    deps = getNodeModulesFile(link)['dependencies']
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


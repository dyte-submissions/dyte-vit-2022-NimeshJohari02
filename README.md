[![open in visual studio code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=7943245&assignment_repo_type=assignmentrepo)
<div id="top">
to run the code first make sure you get the required libraries installed.
<br>
<br>
<a href="https://www.python.org/downloads/">https://www.python.org/downloads/</a>
<!-- code block -->
<pre class="code-block "><code>pip install -r requirements.txt 
</div>
<!-- large text div -->
##<div class="large-text-div">
Since we are planning to run this as a microservice the lesser the storage space and the files it has to fetch it better .
it is for this reason that i have decided to use native libraries for the following:
<br>
<br>
<ul>
####<li> getting args from the cli </li>
####<li> parsing the args and storing them using lists</li>
####<li> not using libraries like pandas or numpy which increase the overall size of the dependencies thus making the entire service charge more . </li>
####<li>trying to fetch the </li>
####<li>Fetching only package.json from the given URL's </li>
####<li> Using github CLI (gh) to fetch the files from the given URL's</li>
<br>
#### To install gh use the following command:
###<br>(For Mine and Arch Based Machines :) 
<br>
##<pre class="code-block "><code>sudo pacman -S github-cli
</div>

<!-- Usage -->
<div class="large-text-div">
<h2>Usage</h2>
For Subtask 1 :
Fetching Dependency and its version from the given URL's Use the below Command 
<pre class="code-block "><code> python app.py -i Dataset.csv axios@0.24.0 
</div>
Output
<div class="large-text-div">
<!-- image -->
<img src="./images/subtask1.png" alt="Subtask1 SS">
</div>
<!-- Large Text -->
<div class="large-text-div">
For information Fetching ie subtask 2
Use the Following command
<pre class="code-block "><code> python app.py -u true -i Dataset.csv axios@0.25.8 nodemon@2.1.1
</pre>
Output
<div class="large-text-div">
<!-- image -->
<img src="./images/subtask2.png" alt="Subtask2 SS">
</div>

<br>
<br>
<br>

<div class="large-text-div">
##<h2>TODO</h2>
<ul>
###<li>Fix JSON Parsing Python Error</li>
###<li>Create Pull Request</li>
<br>
<br>
<br>
<br>
<br>
<!-- Made With Love -->
Made with <i class="fa fa-heart" aria-hidden="true"></i> by <a href="github.com/NimeshJohari02">Nimesh Johari</a>

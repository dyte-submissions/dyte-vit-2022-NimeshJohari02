
# Dyte ToolKit Submission 

Your friendly neighborhood Dependabot clone . Just without the annoying mails and notifications :)

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`GITHUB_AUTH_TOKEN`

`GITHUB_USERNAME`


## Screenshots
For the first subtask ie checking dependencies . 
![App Screenshot](./images/subtask1.png)

For the subtask 2 ie Updating dependencies
![App Screenshot](./images/subtask1.png)



## Run Locally

Clone the project

```bash
  git clone https://github.com/dyte-submissions/dyte-vit-2022-NimeshJohari02
```

Go to the project directory

```bash
  cd dyte-vit-2022-NimeshJohari02/
```

Install dependencies

```bash
    pip install -r requirements.txt
```




# Usage/Examples

```python
# To check for unmet dependencies use the following command 

python app.py -i Dataset.csv axios@0.24.012 node@16.2 react@16.6 ejs@12.1

#Add any number of Libraries and Versions Seperated by " " and Versions by "@"

```
![App Screenshot](./images/subtask1First.png)


![App Screenshot](./images/subtask1Second.png)


```python
# To check for updation of the unmet dependencies use the following command 

python app.py -u true -i Dataset.csv axios@0.24.012 node@16.2 react@16.6 ejs@12.1

#Add any number of Libraries and Versions Seperated by " " and Versions by "@"

```
## Output For subtask 1
![App Screenshot](./images/subtask2First.png)


![App Screenshot](./images/subtask2Second.png)

## Updated dependencies look like these 

![App Screenshot](./images/UpdateDeps.png)

## Pull Request Once Created Can Also be seen from Github

![App Screenshot](./images/Updatepr.png)


## Badges

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)


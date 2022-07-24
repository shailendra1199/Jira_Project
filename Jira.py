#JIRA-PROJECET

from os import remove
import re
from traceback import print_tb
import weakref
import requests
from requests.auth import HTTPBasicAuth
import json
import pandas as pd
import smtplib
import sys
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pretty_html_table import build_table 


# URL to Search all issues.
url = "#JIRA_DOMAIN_NAME/rest/api/2/search"

# Create an authentication object,using
# registered emailID, and, token received.
auth = HTTPBasicAuth("#JIRA_USERNAME",
                    "#JIRA_API_TOKEN")

# The Header parameter, should mention, the
# desired format of data.
headers = {
    "Accept": "application/json"
}
# Mention the JQL query.
# Here, all issues, of a project, are
# fetched,as,no criteria is mentioned.
query = {
    'jql': 'project =#PROJECT_NAME '
}

# Create a request object with above parameters.
response = requests.request(
    "GET",
    url,
    headers=headers,
    auth=auth,
    params=query
)

# Get all project issues,by using the
# json loads method.
projectIssues = json.dumps(json.loads(response.text),
                        sort_keys=True,
                        indent=4,
                        separators=(",", ": "))
# print(projectIssues)

# print(projectIssues)
# The JSON response received, using
# the requests object,
# is an intricate nested object.
# Convert the output to a dictionary object.
dictProjectIssues = json.loads(projectIssues)

# We will append,all issues,in a list object.
listAllIssues = []

# The Issue details, we are interested in,
# are "Key" , "Summary" and "Reporter Name"
# keyIssue, keySummary, keyReporter,keylastupdated,keycreated,keyassignee,keystatus,keyid= "", "", "","","","","",""
keyIssue, keySummary, keyReporter,keylastupdated,keycreated,keyassignee,keystatus,keyid= "", "", "","","","","",""


def iterateDictIssues(oIssues, listInner):

    # Now,the details for each Issue, maybe
    # directly accessible, or present further,
    # in nested dictionary objects.
    for key, values in oIssues.items():

        # If key is 'fields', get its value,
        # to fetch the 'summary' of issue.

        if(key == "fields"):

            # Since type of object is Json str,
            # convert to dictionary object.
            fieldsDict = dict(values)

            # The 'summary' field, we want, is
            # present in, further,nested dictionary
            # object. Hence,recursive call to
            # function 'iterateDictIssues'.
            iterateDictIssues(fieldsDict, listInner)
        
        elif(key=={'fields':'displayName'}):
            
            assigneeDict=dict(values)
            iterateDictIssues(assigneeDict,listInner)

        #status key fetch todo,progress,done
        elif (key=='status'):
            
            statusDict=dict(values)
            iterateDictIssues(statusDict,listInner)


        # If key is 'reporter',get its value,
        # to fetch the 'reporter name' of issue.
        elif (key == "reporter"):

            # Since type of object is Json str
            # convert to dictionary object.
            reporterDict = dict(values)

            # The 'displayName', we want,is present
            # in,further, nested dictionary object.
            # Hence,recursive call to function 'iterateDictIssues'.
            iterateDictIssues(reporterDict, listInner)
    
            

        # Issue keyID 'key' is directly accessible.
        # Get the value of key "key" and append
        # to temporary list object.
        elif(key == 'key'):
            keyIssue = values
            listInner.append(keyIssue)
        #addassignie
        # elif(key=='assignee'):
        
        #     keyassignee=values
        #     listInner.append(keyassignee)   

        # Get the value of key "summary",and,
        # append to temporary list object, once matched.
        elif(key=="name"):
            keystatus=values
            listInner.append(keystatus)
      
        
        elif(key == 'summary'):
            keySummary = values
            listInner.append(keySummary)

        # Get the value of key "displayName",and,
        # append to temporary list object,once matched.
        elif(key == "displayName"):
            keyReporter = values
            listInner.append(keyReporter)

       

        elif(key=='lastViewed'):
            keylastupdated=values
            listInner.append(keylastupdated)

        elif(key=='created'):
            keycreated=values
            listInner.append(keycreated)

    
    

        elif(key=="id"):
            keyid=values
            listInner.append(keyid)

    
#ASSIGNE_EMAIL_ADDRESS
        elif(key=='emailAddress'):
            keyassignee=values
            listInner.append(keyassignee)    

    


# Iterate through the API output and look
# for key 'issues'.
for key, value in dictProjectIssues.items():

    # Issues fetched, are present as list elements,
    # against the key "issues".
    if(key == "issues"):

        # Get the total number of issues present
        # for our project.
        totalIssues = len(value)

        # Iterate through each issue,and,
        # extract needed details-Key, Summary,
        # Reporter Name.
        for eachIssue in range(totalIssues):
            listInner = []

            # Issues related data,is nested
            # dictionary object.
            iterateDictIssues(value[eachIssue], listInner)

            # We append, the temporary list fields,
            # to a final list.
            listAllIssues.append(listInner)

# Prepare a dataframe object,with the final
# list of values fetched.
dfIssues = pd.DataFrame(listAllIssues, columns=["Created","LastUpdated","Reporter","Assignee","issue","Status",
                                                "Summary","id",
                                                "Key"])

# Reframing the columns to get proper
# sequence in output.

columnTiles = ["Key", "id","Summary","Status","issue","Assignee","Reporter","LastUpdated","Created"]
dfIssues = dfIssues.reindex(columns=columnTiles)
#remove status=done row smoothly
# dfIssues=dfIssues[dfIssues['Assignee'] != 'none']
dfIssues=dfIssues[dfIssues['Status'] != 'Done']
print(type(dfIssues))
print(dfIssues)

#send email 
#create email api token for EMAIL Password 


def send_mail(body):
    
    message = MIMEMultipart()
    message['Subject'] = '#SUBJECT'
    message['From'] = '#EMAIL_ID'
    message['To'] = 'TO_EMAIL_ID'

    body_content = body
    message.attach(MIMEText(body_content, "html"))
    msg_body = message.as_string()

    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(message['From'], 'FROM#EMAIL_ID_API_TOKEN')
    server.sendmail(message['From'], message['To'], msg_body)
    server.quit()

def send_country_list():
    gdp_data = dfIssues
    output = build_table(gdp_data, 'blue_light')
    send_mail(output)
    return "Mail sent successfully."

print(send_country_list())

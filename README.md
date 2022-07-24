# Jira_Project
fetch jira tickets details via python
---------------------
Approach:
_____________________
->Import the required modules.\
->Prepare URL, to search, all issues.
->Create an authentication object, using registered emailID, and, token received.
->Pass the project name, in, JQL query. If you, omit JQL query, then, Issues, present, against all projects, on your domain, are obtained.
->Create and send, a request object, using authentication, header objects, and, JQL query.
->Use, JSON loads method, to convert the JSON response, into a Python dictionary object.
->All Issues are present, as list elements, against the key ‘issues’, in the main API output. Hence, loop through each element.
______________________________________________________________________________________________________________

FIELDS TO FILL:
__________________
LINES Change in Jira.py file
****************************
LINE 20 in Jira.py -> #JIRA_DOMAIN_NAME = # URL to Search all issues.
LINE 24 & 25 -> ##JIRA_USERNAME" = # jira username and #JIRA_API_TOKEN 
get Jira api token from-
-----------------------
Create an API token
-----------------------
Create an API token from your Atlassian account:

Log in to https://id.atlassian.com/manage-profile/security/api-tokens.

Click Create API token.

From the dialog that appears, enter a memorable and concise Label for your token and click Create.

Click Copy to clipboard, then paste the token in Jira.py line 24 #JIRA_API_TOKEN


LINE 36 -> #PROJECT_NAME = PROJECT-NAME 
LINE  226 --> #SUBJECT = ENTER EMAIL SUBJECT
LINE 227 --> ENTER EMAIL ID {FROM}
LINE 228 --> ENTER EMAIL ID {TO}
LINE 236 --> FROM#EMAIL_ID_API_TOKEN = ENTER EMAIL ID API TOKEN 
=====DONT USE EMAIL PASSWORD ---

;)


#Developed from Google examplecode: https://github.com/gsuitedevs/python-samples/blob/master/tasks/quickstart/quickstart.py
from __future__ import print_function
import pickle
import os.path
import os
import time
import datetime
import requests, sys, webbrowser
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Read and Write Permission for Google Tasks
SCOPES = ['https://www.googleapis.com/auth/tasks']

#Global Variables
driver = None
select = None
currentMAUnit = None
#Prefix to place infront of automaticaly added tasks, used for both adding and removeing the tasks
prefix = "AUTO:"

def main():
    if getattr(sys, 'frozen', False) :
    # running in a bundle
        chromedriver_path = os.path.join(sys._MEIPASS, 'chromedriver')

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    #Creates an API service for Google Tasks using the Credentials in the token.pickle file
    service = build('tasks', 'v1', credentials=creds)

    #Clears the terminal and prints a welcome message
    os.system('cls||clear')
    print("=================================================================")
    print("|                    Zach's Task Manager                        |")
    print("=================================================================")

    #Prompts for user input to get action
    act = input("Would you like to [view] or [add] or [addwebassign] tasks? ")

    #If user input view, get the tasks from default list and print them
    if act == "view":
        #Retreives tasks
        tasks = service.tasks().list(tasklist='@default').execute()
        #If no tasks are found print that
        if not tasks:
            print("No tasks found")
        #Otherwise print all the tasks in the default list
        else:
            for task in tasks['items']:
                print ("Task: " + task['title'])
                date = task['due'].split("-")
                year = date[0]
                month = date[1]
                dayS = date[2].split("T")
                day = dayS[0]
                print("     Due: " + month + "-" + day + "-" + year)
        input("Press enter to continue ")
        main()
    #If the input is add, prompt for the title and due date and add it to the default list
    elif act == "add":
        tit = input("Title: ")
        date_time_str = input("Due date (MON DD YYYY  H:MMPM): ")
        date_time_obj = datetime.datetime.strptime(date_time_str, '%b %d %Y %I:%M%p')
        add = {
            'title' : tit,
            'notes' : '',
            'due' : date_time_obj.isoformat() + 'Z'
        }
        result = service.tasks().insert(tasklist='@default', body=add).execute()
        #If result is empty there was an error
        if not result:
            print('Could not add')
        #Otherwise print the result id
        else:
            print(result['id'])
    #If the input is exit, exit the program
    elif act == "exit":
        sys.exit()
    #If the input is remove, remove all tasks with the prefix in the default list
    elif act == "remove":
        fullTasks = service.tasks().list(tasklist='@default', showCompleted=True, showHidden=True, maxResults=100).execute()
        found = False
        for task in fullTasks['items']:
            if prefix in task['title']:
                service.tasks().delete(tasklist='@default', task=task['id']).execute()
        print("Removed all automated tasks")
        time.sleep(1)
        main()
    #If the input is removeauth, remove the auth file and reprompt for authorization
    elif act == "removeauth":
        remove()
        main()
    #If the input is addwebassign, scrape webassign for data, get all asignments for each class and add them as tasks
    elif act == "addwebassign":
        currentMAUnit = int(input("What unit are you on in calc? "))
        file = open("pass.txt")
        pas = file.readline()
        driver = webdriver.Chrome()
        driver.set_page_load_timeout("10")
        driver.get("https://www.webassign.net/ncsu/login.html")
        driver.find_element_by_id("loginbtn").click()
        driver.find_element_by_name("j_username").send_keys("zmgrosec")
        driver.find_element_by_name("j_password").send_keys(pas)
        #driver.find_element_by_id("formSubmit").click()
        while True:
            try:
                driver.find_element_by_name("_eventId_proceed").click()
                break
            except Exception as e:
                None
        time.sleep(2)
        print("Adding Courses to Task List...")
        numAdded = 0
        for i in [1] + list(range(1, 4)):
            select = Select(driver.find_element_by_id('courseSelect'))
            select.select_by_index(i)
            currentClass = select.first_selected_option.text.split(",")[0]
            if currentClass == "PY 206" or currentClass == "PY 209":
                continue
            driver.find_element_by_xpath('/html/body/form/div/main/div[1]/div/div/div[1]/nav/div/button').click()
            assignmentList = driver.find_element_by_xpath("/html/body/form/div/main/div[6]/div[1]/div[1]/section/ul")
            assignments = assignmentList.find_elements_by_tag_name("li")
            for assignment in assignments:
                assignmentName = assignment.find_element_by_xpath("a/div/span").text
                assignmentDue = assignment.find_element_by_xpath("a/div[3]").text
                aTS = assignmentDue.split(", ")
                aTHMS = aTS[3].split(" ")
                date_time_obj = datetime.datetime.strptime(aTS[1] + " " + aTS[2] + " " + aTHMS[0] + aTHMS[1], '%b %d %Y %I:%M%p')
                titleC = currentClass + " - " + assignmentName
                add = {
                    'title' : prefix + currentClass + " - " + assignmentName,
                    'notes' : '',
                    'due' : date_time_obj.isoformat() + 'Z'
                }
                fullTasks = service.tasks().list(tasklist='@default', showCompleted=True, showHidden=True, maxResults=100).execute()
                found = False
                for task in fullTasks['items']:
                    if task['title'] == prefix + currentClass + " - " + assignmentName or task['title'] == currentClass + " - " + assignmentName:
                        print("FOUND")
                        found = True
                if found or ignore(assignmentName) or ignoreMA(currentMAUnit, assignmentName):
                    continue
                result = service.tasks().insert(tasklist='@default', body=add).execute()
                if not result:
                    print('Could not add')
                else:
                    numAdded = numAdded + 1
                    print("Added: " + currentClass + " - " + assignmentName)
        print("Total Assignments Added: %i" % (numAdded))
        input("Press enter to quit")
        driver.quit()
        sys.exit()
    #Otherwise the input is not valid and the user is reprmpted
    else:
        print("Not valid input")
        time.sleep(1)
        main()
#================================END MAIN======================================#

#Method to check if the MA assignments need to be ignored, only adding assignments for current unit
def ignoreMA(unit, name):
    if name.find(".") == -1:
        return False
    if unit != int(name[name.find(".") - 1]):
        return True
    return False

#Method to check if the assignment needs to be ignored
#TODO: Implement a file with ignored assignments
def ignore(name):
    if(name == "Access to Calculus 1 (MA 141) Textbook Files"):
        return True
    return False

#Method to remove the auth file
def remove():
    confirm = input("Are you sure you want to remove the auth file? (YES/NO)")
    if confirm == "YES":
        try:
            os.remove('token.pickle')
            sys.exit()
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
            sys.exit()
    else:
        return

if __name__ == '__main__':
    main()

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

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/tasks']

driver = None
select = None
currentMAUnit = None
prefix = "AUTO:"

def main():
    """Shows basic usage of the Tasks API.
    Prints the title and ID of the first 10 task lists.
    """
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

    service = build('tasks', 'v1', credentials=creds)

    os.system('cls||clear')
    print("=================================================================")
    print("|                    Zach's Task Manager                        |")
    print("=================================================================")


    act = input("Would you like to [view] or [add] or [autoadd] tasks? ")

    if act == "view":
        tasks = service.tasks().list(tasklist='@default').execute()

        if not tasks:
            print("No tasks found")
        else:
            for task in tasks['items']:
                print ("Task: " + task['title'])
                date = task['due'].split("-")
                year = date[0]
                month = date[1]
                dayS = date[2].split("T")
                day = dayS[0]
                print("     Due: " + month + "-" + day + "-" + year)

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
        if not result:
            print('Could not add')
        else:
            print(result['id'])
    elif act == "exit":
        exit()
    elif act == "remove":
        fullTasks = service.tasks().list(tasklist='@default', showCompleted=True, showHidden=True, maxResults=100).execute()
        found = False
        for task in fullTasks['items']:
            if prefix in task['title']:
                service.tasks().delete(tasklist='@default', task=task['id']).execute()
        print("Removed all automated tasks")
        time.sleep(1)
        main()
    elif act == "removeauth":
        remove()
        main()
    elif act == "scrape" or act == "autoadd":
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
        #if options.text == "Select an Option":
        #    None
        #else:
        #    select.select_by_visible_text(options.text)
        #    driver.find_element_by_xpath('/html/body/form/div/main/div[1]/div/div/div[1]/nav/div/button').click()
        #    elect = Select(driver.find_element_by_id('courseSelect'))
        #    opt = select.options
        #    input()
        print("Total Assignments Added: %i" % (numAdded))
        input("Press enter to quit")
        driver.quit()
        quit()
    else:
        print("Not valid input")
        time.sleep(1)
        main()
#================================END MAIN======================================#

def ignoreMA(unit, name):
    if name.find(".") == -1:
        return False
    if unit != int(name[name.find(".") - 1]):
        return True
    return False

def ignore(name):
    if(name == "Access to Calculus 1 (MA 141) Textbook Files"):
        return True
    return False

def remove():
    confirm = input("Are you sure you want to remove the auth file? (YES/NO)")
    if confirm == "YES":
        try:
            os.remove('token.pickle')
            exit()
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
            exit()
    else:
        return

if __name__ == '__main__':
    main()
# [END tasks_quickstart]

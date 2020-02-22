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

    # Call the Tasks API
    #results = service.tasklists().list(maxResults=10).execute()
    #items = results.get('items', [])

    os.system('cls||clear')
    print("=================================================================")
    print("|                    Zach's Task Manager                        |")
    print("=================================================================")


    act = input("Would you like to [view] or [add] tasks? ")

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
        remove()
        main()
    elif act == "scrape":
        #testing scrape here
        file = open("pass.txt")
        pas = file.readline()
        driver = webdriver.Chrome()

        driver.set_page_load_timeout("10")
        driver.get("https://www.webassign.net/ncsu/login.html")
        driver.find_element_by_id("loginbtn").click()
        driver.find_element_by_name("j_username").send_keys("zmgrosec")
        driver.find_element_by_name("j_password").send_keys(pas)
        #driver.find_element_by_id("formSubmit").click()
        input("Press enter once you have authenticated");
        driver.find_element_by_name("_eventId_proceed").click()
        time.sleep(2)
        select = Select(driver.find_element_by_id('courseSelect'))
        for options in select.options:
            print(options.text)
            course()
        #driver.find_element_by_xpath('/html/body/form/div/main/div[1]/div/div/div[1]/nav/div/button').click()
        input("Press enter to quit")
        driver.quit()
    else:
        print("Not valid input")
        time.sleep(1)
        main()

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

def course():
    #TODO Implement the scrape of each individual course.

if __name__ == '__main__':
    main()
# [END tasks_quickstart]

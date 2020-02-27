# GoogleTaskManager (ZMGTaskManager)
### Designed by Zach Groseclose
#### Info:
+ [LinkedIn](https://www.linkedin.com/in/zachary-groseclose-0b6317167 "Zach's LinkedIn Profile")
+ [Email: zmgrosec@ncsu.edu](mailto:zmgrosec@ncsu.edu "Zach's Email")
------------------------------------------

### Google Task Manager is a program that will scrape data from WebAssign (potentially WolfWare also) and inport it to the default Google Task list for the current user in the default browser. It is currently a *work in progress*.

------------------------------------------

#### TODO:
+ ~~Add scrape from WebAssign~~ **Done**
+ Add Scrape from WolfWare (Next!)
+ ~~Work on time implementation~~ **Done**
+ ~~Better command line usability~~ **Done**
+ Maybe a GUI/Web interface
+ Add direct download for dist folder

-----------------------------------------

### Instructions

+ Download the repo as a ZIP
+ Extract to folder
+ Create txt file that contains your unity password named "userpass.txt"
  - Unity ID must be on first line
  - Password must be on second line
+ If you have python installed you can run GoogleTaskManager.py
+ Otherwise place the pass.txt file inside the dist folder
+ Run either the py file or the exe through command prompt

-----------------------------------------

### Commands

+ **view** - View the current list of tasks on your default Google Task List
+ **add** - Manually add a task to your default Google Task List
+ **addwebassign** - Scrape NCSU Webassign for current assignments and add them to the default Google Task List (Will have set prefix "AUTO: " this can be changed at the top of the file under prefix = )
+ **remove** - Removes all Google Tasks with the same prefix as the set prefix. Will remove all tasks if no prefix is set.
+ **removeauth** - Removes the authorization file. Use this command if you want to use a different account on the same computer.

------------------------------------------

### Other notes

+ Currently the OAuth file only works for users within the ncsu.edu domain, working towards approval for public use, although it would be silly since it currently only works with NCSU WebAssign.
+ If you find any bugs or issues feel free to post them under the issues tab on GitHub.

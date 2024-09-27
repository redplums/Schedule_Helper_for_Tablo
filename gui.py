import csv

import eel
import os
import sys
import platform
import datetime
import time
import requests


global num_days
num_days = 7

eel.init("web")

@eel.expose
def refresh():
    p = time.ctime(os.path.getmtime('scheduled.csv'))
    print(p)
    return p

# Exposing the random_python function to javascript
@eel.expose	
def Tablo_IP():
    print("Enter Tablo IP Address")
    with open('config.txt', mode ='r')as file:
        reader = file.readline()
    file.close
    reader = reader[19:]
    print(reader)
    return reader

@eel.expose	
def change_IP(q):
    print("Tablo IP Address is changing to " + q)
    if len(q.strip())<8:
        print("Seems you mistyped.  Need at least 8 characters (including '.') for IP address")
    else:
        with open('config.txt', mode ='w', newline='')as file:
            file.write("Tablo IP Address:  " + q)
            file.close()
   # with open('config.txt', mode ='r')as file:
   #     reader = file.readline()
   # file.close
   # reader = reader[19:]
   # print(reader)
   # return reader
    
            
def print_JS_value(n):
    print(n)


# Exposing the random_python function to javascript
@eel.expose	
def keywords():
    print("View/Edit Keywords for Search")
    with open('keyword_search.csv', mode ='r')as file:
        reader = csv.reader(file, delimiter=';')
        rows = list(reader)
        num_rows = len(rows)
        for i in range(num_rows):
            print(rows)
            return rows
        file.close
            
def print_JS_value(n):
    print(n)



@eel.expose
def delete_item(x):
    with open('keyword_search.csv', mode ='r')as file:
        reader = csv.reader(file, delimiter=';')
        rows = list(reader)
        print(x)
        x = int(x)
        print(rows[x])
        del_item=rows[x]
        del rows[x]
        print(rows)
    os.remove('keyword_search.csv')    
    with open('keyword_search.csv', mode ='w', newline='')as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(rows)
    return del_item

@eel.expose
def add_item(y, k):
    print(y, k)
    if len(y.strip())<1:
        print("Need at least 2 characters for keyword")
    else:
        with open('keyword_search.csv', mode ='a', newline='')as file:
            reader = csv.reader(file, delimiter=';')
            new_add = [y, k]
            csvwriter = csv.writer(file)
            csvwriter.writerow(new_add)
            file.close()
#        eel.say_hello_js('Python')
#        del rows[x]
#        print(rows)

@eel.expose
def scheduled():
    print("Scheduled Items from Last Scan")
    with open('scheduled.csv', mode ='r')as file:
        reader = csv.reader(file, delimiter=',')
        rows = list(reader)
        num_rows = len(rows)
        for i in range(num_rows):
            print(rows)
            return rows
        file.close

@eel.expose
def num(n):
    global num_days
    num_days = n
    print(num_days)
    
@eel.expose
def search():
    print("Searching guide listings now...")
    time.sleep(1)
    global num_days
    num_days = num_days
    with open('Search_Schedule.py', 'r') as f:
        exec(f.read(), globals(), locals())
    

#    with open('scheduled.csv', mode ='r')as file:
#        reader = csv.reader(file, delimiter=',')
#        rows = list(reader)
#        num_rows = len(rows)
#        for i in range(num_rows):
#            print(rows)
#            return rows
#        file.close
    
###
###  This code is not setup to run in the GUI.  It is commented out in the html file.
###  os.system(r'SchTasks /Create /SC DAILY /TN "My Task" /TR "C:mytask.bat" /ST 09:00')
###
@eel.expose
def windows_sched(t):
    print("This will setup a task in MS Scheduler to run the program daily")
    print(t)
    if int(t)<10: t = str("0" + t)
    # to get the location of the current python file
    basedir = os.path.dirname(os.path.abspath(__file__))
    # to join it with the filename
    categorization_file = os.path.join(basedir,'shft.bat')
    print(categorization_file)
    os.system(r'SchTasks /Create /SC DAILY /TN "Schedule Helper for Tablo" /TR "' + categorization_file + '" /ST ' + t + ':00')
    print('SchTasks /Create /SC DAILY /TN "Schedule Helper for Tablo" /TR "' + categorization_file + '" /ST ' + t + ':00')
# this depends on having a file named shft.exe in same folder   



# Start the index.html file
try:
    eel.start('index.html', mode='chrome-app', size=(300, 200))
except EnvironmentError:
    # If Chrome isn't found, fallback to Microsoft Edge on Win10 or greater
    if sys.platform in ['win32', 'win64'] and int(platform.release()) >= 10:
        eel.start('main.html', mode='edge')
    else:
        raise

###
### guide on creating exe file, https://www.tomshardware.com/how-to/create-python-executable-applications
###  Did up to 'Create a Test Script' step 3  

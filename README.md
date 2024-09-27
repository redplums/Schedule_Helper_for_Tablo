# Schedule_Helper_for_Tablo
Schedule_Helper_for_Tablo (SHfT) is a Python 3 program that allows you to search for keywords in the Tablo DVR guide data and schedule recordings based on those keywords.  
#### Requirements
* Python 3 (tested with Python 3.10)
* Legacy Tablo (**not** a Tablo Gen 4)
	* Author only tested with Tablo 2-tuner network model with guide subscription
* Recommended - assign your Tablo a static IP on your home network, otherwise the program will not work if the IP address changes without re-entry

### Usage
The repository includes a web-based GUI using the eel library for Python.  This is not required to use the program, but offers a more user-friendly way to setup and manage the keywords and frequency of searches.  The web-based GUI was developed and used on a Windows 10 PC.

#### Using the web-based GUI:
* Run gui.py in Python 3
* Webpage opens with title **Tablo Schedule Helper**
* To use:
	* Refresh - click to show last date search was run
	* View Tablo IP Address - click to display the Tablo IP address that has been configured for this program
* Enter Tablo IP Address - click to change the IP address used by the program to direct it to your Tablo (**must do** first time you run the program!)
* View/Edit Keywords for Search - Displays list of keywords and categories; click "-" to delete an item from the list
* Add Keyword - click to add a new keyword or phrase (such as Jimmy Fallon); after submitting it will ask you to select the type of program to limit the search to (TV Series, Movies, Sports, or All the above) - this is useful when you want to record movies with Jimmy Fallon but not record TV series like the Tonight Show with Jimmy Fallon
* View Scheduled Recordings - this brings up a list of recordings that have been initiated by the program; it is a running list kept locally and does not reflect the status of the recording on the Tablo DVR
* Number of Days to Search - searching through the entire 14 day guide can take some time, so this allows you to limit the number of days it will search; several options are given from 1 to 14 days; default is 7 days; this field only used when Run Search button is used
* Run Search - click to run program **now** to search for keywords and schedule recordings

#### Using without the web-based GUI:
* The program can be run and does not require a browser or display.  
* Open config.txt and enter your Tablo's local IP address.  The program will not work if the IP address is not correct.  
* The web folder and gui.py are not used without the GUI and can be deleted.  
* Open keyword_search.csv to create your list of keywords.  Use a semicolon and also include 'series', 'movie', 'sports', or 'all' for the category you want to limit the search to.  Use the examples as a guide ([Don Cheadle; all] [Adam Sandler; movie] [Andy Samberg; series] [Carolina Panthers; sports])
* File scheduled.csv used to keep track of what the recordings were scheduled by the program.  This is a local copy and is not updated by changes to your Tablo DVR recordings.
* File lastscanairings.csv is a record of the paths of the airings when the last search was conducted.  Plan is to use this for future optimization.
* Run Search_Schedule.py to conduct keyword search and schedule recordings.  
* If you are interested in scheduling a regular search, use tools like cron in Linux or Task Scheduler in Windows.  Remember, guide data is only updated once a day so definitely no reason to run more often than that.  That said, broadcast programming can change.  For example, the teams for a sporting event broadcast in your area may not be decided 14 (or even 7) days beforehand.  
* Default number of search days is 7.  Depending on your usage, you may want to change this value.  This can be changed in Search_Schedule.py line 63 "num_days".  The number of channels you have and the number of keywords you're searching for impact how long it takes the program to run.  Reducing the number of search days will shorten the run time needed.  I recommend keeping the number of search days low and instead schedule the program to run daily.  

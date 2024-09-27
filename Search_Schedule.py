import time
import datetime
import requests
import json
import traceback
import csv
import re

import eel
import os
import sys
import platform

     
'''
Program works to review list of keywords (keyword_search.csv) and schedules those airings that have a match to record.  
Search works differently depending on type of program.
Movies:  compare keyword against cast and director for listings of movies
Series:  compare keyword against title and description for episode (cast is in the series information, so guests and guest stars are only noted in the episode information)
Sports:  compare keyword against title and description for event

To Do:
    Give message if IP is not configured in config.txt
    How to search all recordings if num_day is 14
        

'''

start = time.perf_counter()


# Tablo IP must be entered in config.txt.  Pulls that info from that file.  
global private_ip

with open('config.txt') as f:
    private_ip = f.readline()
f.close
private_ip = private_ip[19:]
private_ip = private_ip.strip()
print(private_ip)

# Establish how to connect to Tablo and pulls listing of recordings and upcoming airings.
class TabloDevice:
    port = 8885
    IP = private_ip
    address = str('{0}:{1}'.format(IP, port))
    dataIP = requests.get('http://{0}/server/info'.format(address))
    dataIP = dataIP.json()
    recordings = requests.get('http://{0}/guide/series'.format(address))
    recordings = recordings.json()
    recordings_count = len(recordings)
    airings = requests.get('http://{0}/guide/airings'.format(address))
    airings = airings.json()
    airings_count = len(airings)

USER_AGENT = 'Tablo-Py/0.1'
head = {'User-Agent': USER_AGENT}

global airing_datetime_clean

# Number of days to search airings (assumes listing is chronological order)
if 'num_days' not in globals():
    num_days = 7
else:
    num_days = num_days
num_days = int(num_days)

now = datetime.datetime.now(datetime.timezone.utc)
end_day = now + datetime.timedelta(days=num_days)
end_day = datetime.datetime.timestamp(end_day)
print(num_days)
print(end_day)

airing_datetime_clean = datetime.datetime.timestamp(now)

#Counters for how many airings were searched
movie_count = 0
series_count = 0
sports_count = 0
added_schedule = 0

#Separating airings list into movies, series, and sport
movie_airings = [x for x in TabloDevice.airings if "movie" in x]
series_airings = [x for x in TabloDevice.airings if "series" in x]
sports_airings = [x for x in TabloDevice.airings if "sports" in x]

print("Number of items in airings:  " + str(TabloDevice.airings_count))

# read keyword_search.csv to get keywords and categories for search
with open('keyword_search.csv', mode ='r')as file:
    reader = [row["Keywords"] for row in csv.DictReader(file, delimiter=";")]
    file.close()
with open('keyword_search.csv', mode ='r')as file:
    cat = [row["Category"] for row in csv.DictReader(file, delimiter=";")]
    file.close()

#Search movies
num_movies = len(movie_airings)
print("Number of movies in airings:  " + str(num_movies))
top_h_range = num_movies / 50
top_h_range = int(top_h_range+1)
#This if statement essentially skips this category if no keyword categories are 'movie' or 'all'
if 'movie' and 'all' not in cat:
    top_h_range = 1
for h in range(1, top_h_range):
    step_movies = h
    episode =  movie_airings[((50*step_movies)-50):((50*step_movies)-1)]
    episode_str = str(episode)
    episode_IP = 'http://{0}/batch'.format(TabloDevice.address)
    jsone = requests.post(episode_IP, data=episode_str)
    episode_json = jsone.json()
    movie_list = []
    for i in range(0+(50*(h-1)),49+(50*(h-1)),1):
        movie_path = episode_json[movie_airings[i]]["movie_path"]
        movie_list.append(movie_path)

    movie_list_str=str(movie_list)
    movie_info_IP = requests.post(episode_IP, data=movie_list_str)
    print("### " + str(h) + " searching movies")
    movie_info_json = movie_info_IP.json()
    movie_count = movie_count + 50
    for j in range(len(cat)):
        if str(cat[j]) in ("movie") or str(cat[j]) in ("all"):
            if str(reader[j]) in str(movie_info_json):
                for k in range(0+(50*(h-1)),49+(50*(h-1)),1):
                    movie_i = str(movie_list[k-(50*(h-1))])
                    movie_request = requests.get('http://{0}'.format(TabloDevice.address) + movie_i)
                    movie_request_json = movie_request.json()
                    episode_showname = movie_request_json["movie"]["title"]
                    episode_movie_path = movie_request_json["path"]
                    episode_year = movie_request_json["movie"]["release_year"]
                    episode_rating = movie_request_json["movie"]["film_rating"]
                    episode_quality = movie_request_json["movie"]["quality_rating"]
                    episode_scheduled = episode_json[movie_airings[k]]["schedule"]["state"]
                    episode_airing_datetime = episode_json[movie_airings[k]]["airing_details"]["datetime"]
                    search_score = 0
                    # check csv for keywords, if match with program info flag to record...
                    if reader[j] in movie_request_json["movie"]["cast"]: search_score = 1
                    if reader[j] in movie_request_json["movie"]["directors"]: search_score = 1
                    # ... but if any airing of this is scheduled to record, don't bother recording...
                    if movie_request_json["show_counts"]["scheduled_count"]>0 : search_score = 0
                    # ... or if there is already a recording, don't bother recording...
                    if movie_request_json["recordings_path"] != None : search_score = 0
                    if search_score > 0:
                    # set program to record
                        movie_airing = episode_json[movie_airings[k]]
                        print(episode_showname + ": " + " with " + reader[j])
                        print("path: " + movie_i)
                        episode_path = 'http://{0}/'.format(TabloDevice.address) + movie_airings[k]
                        episode_path_json = requests.get(episode_path)
                        episode_path_json = episode_path_json.json()
                        episode_path_json['scheduled'] = True
                        record = requests.patch(episode_path, headers=head, json=episode_path_json)
                        print(record)
                        added_schedule = added_schedule + 1
                    # store data to identify movie
                    # write airing information to a file
                        csv_list = [(reader[j]), (episode_showname), (episode_year), (episode_rating), (episode_quality), (episode_scheduled), (episode_airing_datetime)]
                        with open('scheduled.csv', 'a', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerows([csv_list])
                    else:
                        pass                    
            else:
                pass
        else:
            pass

## Break loop if airing date is greater than end_day picked
    p = episode_json[movie_airings[((50*step_movies)-2)]]["airing_details"]["datetime"]
    p = datetime.datetime.strptime(p, "%Y-%m-%dT%H:%MZ")
    p = p.replace(tzinfo=datetime.timezone.utc).timestamp()
    if p > end_day: break

#Search series/episodes
num_series = len(series_airings)
print("Number of series in airings:  " + str(num_series))
top_h_range = num_series / 50
top_h_range = int(top_h_range+1)
if 'series' and 'all' not in cat:
    top_h_range = 1
for h in range(1, top_h_range):
    step_series = h
    episode =  series_airings[((50*step_series)-50):((50*step_series)-1)]
    episode_str = str(episode)
    episode_IP = 'http://{0}/batch'.format(TabloDevice.address)
    jsone = requests.post(episode_IP, data=episode_str)
    episode_json = jsone.json()
    print("### " + str(h) + " searching TV series")
    series_count = series_count + 50
    for j in range(len(cat)):
        if str(cat[j]) in ("series") or str(cat[j]) in ("all"):
            if str(reader[j]) in str(episode_json):
                for k in range(0+(50*(h-1)),49+(50*(h-1)),1):
                    series_i = str(series_airings[k])
                    series_request = requests.get('http://{0}'.format(TabloDevice.address) + series_i)
                    series_request_json = series_request.json()
                    episode_showname = series_request_json["airing_details"]["show_title"]
                    episode_movie_path = series_request_json["path"]
                    episode_year = series_request_json["episode"]["orig_air_date"]
                    episode_rating = series_request_json["episode"]["title"]
                    if episode_rating == None:  episode_rating = "none"
                    episode_quality = series_request_json["episode"]["description"]
                    if episode_quality == None:  episode_quality = "none"
                    episode_scheduled = series_request_json["schedule"]["state"]
                    episode_airing_datetime = series_request_json["airing_details"]["datetime"]
                    search_score = 0
                    # check csv for keywords, if match with program info flag to record...
                    if reader[j] in episode_rating: search_score = 1
                    if reader[j] in episode_quality: search_score = 1
                    # ... but if any airing of this is scheduled to record, don't bother recording...
                    # this doesn't apply since their is no "scheduled_count" for an episode, only for a series
                    #if movie_request_json["show_counts"]["scheduled_count"]>0 : search_score = 0
                    # ... or if there is already a recording, don't bother recording...
                    # this doesn't apply since their is no "recordings_path" for an episode, only for a series
                    #if movie_request_json["recordings_path"] != None : search_score = 0
                    if search_score > 0:
                    # set program to record
                        print(episode_showname + ": " + " with " + reader[j])
                        print("path: " + series_i)
                        episode_path = 'http://{0}/'.format(TabloDevice.address) + series_airings[k]
                        episode_path_json = requests.get(episode_path)
                        episode_path_json = episode_path_json.json()
                        episode_path_json['scheduled'] = True
                        record = requests.patch(episode_path, headers=head, json=episode_path_json)
                        print(record)
                        added_schedule = added_schedule + 1
                    # store data to identify episode
                    # write airing information to a file
                        csv_list = [(reader[j]), (episode_showname), (episode_year), (episode_rating), (episode_quality), (episode_scheduled), (episode_airing_datetime)]
                        with open('scheduled.csv', 'a', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerows([csv_list])
                    else:
                        pass                    
            else:
                pass
        else:
            pass                  

## Break loop if airing date is greater than end_day picked
    p = episode_json[series_airings[((50*step_series)-2)]]["airing_details"]["datetime"]
    p = datetime.datetime.strptime(p, "%Y-%m-%dT%H:%MZ")
    p = p.replace(tzinfo=datetime.timezone.utc).timestamp()
    if p > end_day: break

#Search sporting events
num_sports = len(sports_airings)
print("Number of sports in airings:  " + str(num_sports))
top_h_range = num_sports / 10
top_h_range = int(top_h_range+1)
if 'sports' and 'all' not in cat:
    top_h_range = 1
for h in range(1, top_h_range):
    step_sports = h
    episode =  sports_airings[((10*step_sports)-10):((10*step_sports)-1)]
    episode_str = str(episode)
    episode_IP = 'http://{0}/batch'.format(TabloDevice.address)
    jsone = requests.post(episode_IP, data=episode_str)
    episode_json = jsone.json()
    print("## " + str(h) + " searching sporting events")
    sports_count = sports_count + 10
    for j in range(len(cat)):
        if str(cat[j]) in ("sports") or str(cat[j]) in ("all"):
            if str(reader[j]) in str(episode_json):
                for k in range(0+(10*(h-1)),9+(10*(h-1)),1):
                    sports_i = str(sports_airings[k])
                    sports_request = requests.get('http://{0}'.format(TabloDevice.address) + sports_i)
                    sports_request_json = sports_request.json()
                    episode_showname = sports_request_json["airing_details"]["show_title"]
                    episode_sports_path = sports_request_json["path"]
                    episode_year = sports_request_json["airing_details"]["datetime"]
                    episode_rating = sports_request_json["event"]["title"]
                    if episode_rating == None:  episode_rating = "none"
                    episode_quality = sports_request_json["event"]["description"]
                    if episode_quality == None:  episode_quality = "none"
                    episode_scheduled = sports_request_json["schedule"]["state"]
                    episode_airing_datetime = sports_request_json["airing_details"]["datetime"]
                    search_score = 0
                    # check csv for keywords, if match with program info flag to record...
                    if reader[j] in episode_rating: search_score = 1
                    if reader[j] in episode_quality: search_score = 1
                    # ... but if any airing of this is scheduled to record, don't bother recording...
                    # this doesn't apply since their is no "scheduled_count" for an event, only for the broader category (ie College Basketball)
                    #if movie_request_json["show_counts"]["scheduled_count"]>0 : search_score = 0
                    # ... or if there is already a recording, don't bother recording...
                    # this doesn't apply since their is no "recordings_path" for an event, only for the broader category
                    #if movie_request_json["recordings_path"] != None : search_score = 0
                    if search_score > 0:
                    # set program to record
                        print(episode_showname + ": " + " with " + reader[j])
                        print("path: " + sports_i)
                        episode_path = 'http://{0}/'.format(TabloDevice.address) + sports_airings[k]
                        episode_path_json = requests.get(episode_path)
                        episode_path_json = episode_path_json.json()
                        episode_path_json['scheduled'] = True
                        record = requests.patch(episode_path, headers=head, json=episode_path_json)
                        print(record)
                        added_schedule = added_schedule + 1
                    # store data to identify event
                    # write airing information to a file
                        csv_list = [(reader[j]), (episode_showname), (episode_year), (episode_rating), (episode_quality), (episode_scheduled), (episode_airing_datetime)]
                        with open('scheduled.csv', 'a', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerows([csv_list])
                    else:
                        pass                    
            else:
                pass
        else:
            pass                  

## Break loop if airing date is greater than end_day picked
    p = episode_json[sports_airings[((10*step_sports)-2)]]["airing_details"]["datetime"]
    p = datetime.datetime.strptime(p, "%Y-%m-%dT%H:%MZ")
    p = p.replace(tzinfo=datetime.timezone.utc).timestamp()
    if p > end_day: break

# Print counts for results from search
print("Searched " + str(movie_count) + " movie listings!")
print("Searched " + str(series_count) + " TV series episodes listings!")
print("Searched " + str(sports_count) + " sporting event listings!")
with open('lastscanairings.csv', 'w+', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(TabloDevice.airings)
if added_schedule > 0:
    print("Added " + str(added_schedule) + " recordings to your DVR schedule!")
else:
    print("Nothing matched your search.  No new recordings added to your DVR schedule :(")
    modTime = time.localtime()
    modTime = time.mktime(modTime)
    print(modTime)
    os.utime('scheduled.csv', (modTime, modTime))

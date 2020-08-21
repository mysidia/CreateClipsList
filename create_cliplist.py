#!/usr/bin/python
# create_cliplist 0.1
#
# (C) Mysidia  June 2020, All Rights Reserved.
# Dev/Experimental command line tool
#
# Requires Python language Version 3.x
#
#  This script creates a .CSV file containing information about all a channel's clips
#
#  This then creates a a .TXT file with each line containing the HTTPS:// link to a clip
#
#  This is written in Python-3 on a Linux system and needs the following Python3 libraries installed:
#     requests,  json,  csv
#
#  Developers need an API project on Twitch's website for management tools
#  and the credentials  which are a Client_Id and Client_Secret
#   https://dev.twitch.tv/console
#

import requests
import json
import csv
import os
import time

import apptoken
readTokens = apptoken.get_tokens()
client_id = readTokens[0]
client_secret = readTokens[1]
app_token = readTokens[2]

channel_name = input('Enter the Twitch channel name:')  
lookup_request = requests.get('https://api.twitch.tv/helix/users?login=' + channel_name, headers = {'Client-ID' : client_id,  'Authorization' : 'Bearer ' +app_token})

if lookup_request.status_code == 200:
    j1 = json.loads(lookup_request.text)
    broadcaster_id = j1["data"][0]["id"]
    try:
        with open(j1["data"][0]["login"] + ".txt", 'w') as outfile:
            outfile.write(lookup_request.text + "\n")
            print("Writing broadcaster info for %s -  user-id %s to %s\n" % ( j1["data"][0]["display_name"] , j1["data"][0]["id"] , j1["data"][0]["login"] + ".txt"   ))
    except RuntimeError:
        print("Error: " + sys.exc_info()[0] + "\n")
else:
    raise Exception("Could not lookup broadcaster_id: " + str(lookup_request.text))	
    
print ("Ok, " + channel_name +  " is  broadcaster_id=" + broadcaster_id)
csvfilename = 'clips_' + broadcaster_id + '.csv'
urlfilename = 'clipurls_' + broadcaster_id + '.txt'

print ("Creating " + csvfilename + '.new')    


with open(csvfilename + '.new', 'w', newline='') as csvfile, open(urlfilename + '.new', 'w') as urlfile:
    fieldnames=['id', 'url', 'created_at', 'view_count', 'game_id', 'creator_name', 'video_id', 'broadcaster_name', 'title', 'broadcaster_id', 'creator_id', 'thumbnail_url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    after_string = ""

    while 1 :
       time.sleep(1.2)
       print("Fetching " + 'https://api.twitch.tv/helix/clips?broadcaster_id=' + broadcaster_id + '&first=100' + after_string)
       clipreply = requests.get('https://api.twitch.tv/helix/clips?broadcaster_id=' + broadcaster_id + '&first=100' + after_string, headers = {'Client-ID' : client_id,  'Authorization' : 'Bearer '+app_token})
       j1 = json.loads(clipreply.text)
       print("Writing " + str(len(j1["data"]))  +  " clip URLs to " + csvfilename + ".new" +  " : ")
       for row in j1["data"]:
           urlfile.write(row["url"] + "\n")
           writer.writerow({ "id" : row["id"],
                             "url" : row["url"],
                             "created_at" : row["created_at"],
                             "view_count" : row["view_count"],
                             "game_id" : row["game_id"],
                             "creator_name" : row["creator_name"],
                             "video_id" : row["video_id"],
                             "broadcaster_name" : row["broadcaster_name"],
                             "title" : row["title"],
                             "broadcaster_id" : row["broadcaster_id"],
                             "creator_id" : row["creator_id"],
                             "thumbnail_url" : row["thumbnail_url"] })
       if j1["pagination"] :
           after_string = '&after=' + j1["pagination"]["cursor"]
       else:
           break
       if len(j1["data"]) < 1 :
           break
       time.sleep(4) # Wait 4 seconds b/w requests as a precaution
    print("os.rename() " + csvfilename + '.new -> ' + csvfilename)
    os.rename(csvfilename + '.new', csvfilename)
    #
    print("os.rename() " + urlfilename + '.new -> ' + urlfilename)
    os.rename(urlfilename + '.new', urlfilename)





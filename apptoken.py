#!/usr/bin/python
# apptoken 0.1
#
# (C) Mysidia June 2020, All Rights Reserved.
#
# Requires Python language Version 3.x

# Quick and dirty Twitch API Token credential management
# just saves and loads the credentials to a file in the present directory 
# named  twsecrets
#
# The Client_Id and Client_Secret  are used to create an Application Token.
# Twitch expires Application Tokens after 60 days, so we need to have a check
# to ensure validity and autogenerate a new token if the saved one is no longer valid.
#  
import requests
import json
import csv
import os
import time
import sys

TWSECRETS_FILE = 'twapisecrets.dat'


def get_tokens():
    tempval = int(time.time())
    twsecrets_tempfile = "%s.new%d" % (TWSECRETS_FILE, tempval)
    client_id=""
    client_secret=""
    app_token=""
    try:
        with open(TWSECRETS_FILE, 'r') as secretfile:
            client_id = secretfile.readline().rstrip()
            client_secret = secretfile.readline().rstrip()
            app_token = secretfile.readline().rstrip()
    except:
        print("Unable to read Twitch API secrets from %s\n" % TWSECRETS_FILE)
    validToken = 0

    if client_secret=="":
        print("Please enter client_id and client_secret for the Twitch API access from app on your Twitch dev console https://dev.twitch.tv/console")
        client_id=input("Twitch API Client-ID:")
        client_secret=input("Twitch API Client-Secret:")

    # To get  App token
    # POST to 'https://id.twitch.tv/oauth2/token?client_id=XXX&client_secret=YYYY&grant_type=client_credentials'
    # The reply will look like
    # {"access_token":"secret app auth token here","expires_in":50000,"token_type":"bearer"}
    # app_token = 'a*****************************x'

    validateRequest = requests.get('https://id.twitch.tv/oauth2/validate', headers = {'Client-ID' : client_id,  'Authorization' : 'OAuth ' +app_token})
    if validateRequest.status_code == 200 :
        validToken = 1
    if validToken == 0 :
        tokenRequest = requests.post('https://id.twitch.tv/oauth2/token?client_id=' + client_id +'&client_secret=' + client_secret + '&grant_type=client_credentials')
        if tokenRequest.status_code == 200:
            j = json.loads(tokenRequest.text)
            atoken = j["access_token"]
            app_token = atoken
            try:
                with open(twsecrets_tempfile, 'w') as soutfile:
                    soutfile.write(client_id + "\n")
                    soutfile.write(client_secret + "\n")
                    soutfile.write(app_token + "\n")
                os.rename(twsecrets_tempfile, TWSECRETS_FILE)
            except:
                try:
                    print("Error saving secrets to file: %s.\n" % sys.exc_info()[0])
                    os.unlink(twsecrets_tempfile);
                except:
                    pass
    return [client_id, client_secret, app_token]



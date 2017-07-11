# this is the library file that is imported by another python script
# depends upon the python library 'requests' http://docs.python-requests.org/en/latest/
# see 'testfile.py' for example invocation

THINGSPEAK_URL = 'http://api.thingspeak.com/update'

import requests

# method to post to thingspeak
def post(key, content):

    # create a dictionary with the api key
    key = {'api_key': key}

    # add the content to be posted to the dictionary
    payload = dict(key, **content)

    # post to thingspeak, using the params in the dictionary
    r = requests.post(THINGSPEAK_URL, params=payload)

    # get the response code
    print("Thingspeak POST response:", r.status_code)

    # get the channel entry number
    print("Thingspeak channel entry:", int(r.content))

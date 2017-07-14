# this is the library file that is imported by another python script
# depends upon the python library
# 'httplib' https://pypi.python.org/pypi/httplib2/0.9.1
# and
# 'urllib' https://docs.python.org/2/library/urllib.html
#
# thr v1.0 2017-07-14
#

THINGSPEAK_URL = 'api.thingspeak.com:443'

import httplib, urllib

# method to post to thingspeak
def post(key, content):

    # create a dictionary with the api key
    key = {'api_key': key}

    # add the content to be posted to the dictionary
    payload = dict(key, **content)
    # populate payload 
    params = urllib.urlencode(payload)     
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    # connect to thingspeak using https 
    conn = httplib.HTTPSConnection(THINGSPEAK_URL)   
    # post to thingspeak, using payload 
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
#        print params
        print response.status, response.reason
        data = response.read()
        conn.close()
    # error connection failed    
    except:
        print "connection failed"             

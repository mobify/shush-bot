import json
import urllib2

PROTOCOL = 'http'
SERVER_URL = '10.10.1.47:5001'

def update_config(shushbot_id):
    print '\n\n Updating config...\n\n\n'

    # Build uri
    url = PROTOCOL + "://" + SERVER_URL + "/bots/1/configuration?uuid=" + str(shushbot_id)

    # Grab data
    data = json.load(urllib2.urlopen(url))
    # data = {
    #     "threshold": -7,
    #     "volume": 50
    # }
    print data

    return data['threshold'], 50

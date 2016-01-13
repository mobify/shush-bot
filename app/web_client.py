import json
import urllib2
from threading import Timer

PROTOCOL = 'http'
SERVER_URL = '10.10.1.47:5001'

local_state = {
    "threshold": 0,
    "volume": 50
}

def update_config(shushbot_id):
    print '\n\n Updating config...\n\n\n'

    try:
        # Build uri
        url = PROTOCOL + "://" + SERVER_URL + "/bots/1/configuration?uuid=" + str(shushbot_id)

        # Grab data
        data = json.load(urllib2.urlopen(url))

        print data

        local_state.update({
            "threshold": data['threshold'],
            "volume": data['volume']
        })
    except:
        print "Failed to update."

    Timer(10, update_config, [shushbot_id]).start()

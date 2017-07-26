import httplib2  # http client library in python
import json  # converting in memory python objects to a serialized JSON representation

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

"""
Takes an input string that is the name for the place we want the coordinates for
"""


def getGeocodeLocation(inputString):
    google_api_key = 'AIzaSyCTaz6ny1TsesGRvJgvm6DKcPrRolGWJgo'
    locationString = inputString.replace(" ", "+")
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' %
           (locationString, google_api_key))
    h = httplib2.Http()

    # will return an array with 2 values [HttpResponse, content]
    response, content = h.request(url, "GET")
    result = json.loads(content)  # load as JSON on the content
    # print "response header: %s \n \n " % response
    # return result
    lat = result['results'][0]['geometry']['location']['lat']
    lng = result['results'][0]['geometry']['location']['lng']
    return (lat, lng)


# print getGeocodeLocation("Queens, New York")

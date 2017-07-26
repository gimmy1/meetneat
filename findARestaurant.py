from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = 'XCPHQKTMT3N2NWZMWG2BCQ40GHHRD0LBBVZRU354ZVMEUZ25'
foursquare_client_secret = 'ZC53KE1SVSTOSKR2FPQXIMSGEXC3BVCZTRGBGRUGZZWXLJHE'

"""
1. Geocode the location
2. Search for Restaurants through lat/lng
3. Parse response and return one restaurant
"""


def findARestaurant(mealType, location):
    # 1. Use getGeocodeLocation to get the latitude and longitude coordinates
    # of the location string.
    latitude, longitude = getGeocodeLocation(location)
    # 2. Use foursquare API to find a nearby restaurant with the latitude,
    # longitude, and mealType strings
    url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20130815&ll=%s,%s&query=%s' %
           (foursquare_client_id, foursquare_client_secret, latitude, longitude, mealType))
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # return result
    if result['response']['venues']:
        # return "YES"
        # return result['response']['venues'][0]
        # 3. Grab the first Restaurant
        restaurant = result['response']['venues'][0]
        venue_id = restaurant['id']
        restaurant_name = restaurant['name']
        restaurant_address = restaurant['location']['formattedAddress']
        # return restaurant_address
        address = ''
        for i in restaurant_address:
            address += i

        restaurant_address = address
        # return restaurant_address
        # 4. Get a  300x300 picture of the restaurant using the venue_id (you
        # can change this by altering the 300x300 value in the URL or replacing
        # it with 'orginal' to get the original picture
        url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&v=20150603&client_secret=%s' %
               ((venue_id, foursquare_client_id, foursquare_client_secret)))
        result = json.loads(h.request(url, 'GET')[1])

        # 5.  Grab the first image
        if result['response']['photos']['items']:
            firstpic = result['response']['photos']['items'][0]
            prefix = firstpic['prefix']
            suffix = firstpic['suffix']
            imageURL = prefix + "300x300" + suffix
        else:
            # 6.  if no image available, insert default image url
            imageURL = "http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct"

        # 7.  return a dictionary containing the restaurant name, address, and
        # image url
        restaurant_info = {'name': restaurant_name,
                           'address': restaurant_address, 'image': imageURL}
        return restaurant_info
    else:
        print "No Restaurants Found for %s" % location
        return "No Restaurants Found"


if __name__ == "__main__":
    print findARestaurant("Pizza", "Tokyo, Japan")

# print findARestaurant("steak", 'Dallas, Texas')

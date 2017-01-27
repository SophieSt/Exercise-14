# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 16:07:12 2017

@author: ubuntu
"""

from twython import Twython
import json
import folium
import re

##initiating Twython object 
#twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

##TODO:  This should work as an alternative but it doesn't. Need to find out why
twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()
print ACCESS_TOKEN
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)


def twitter_map_locations(criterion, location = None, count = 1000):
    # This function creates an html map from tweets
    # criterion matching tweet
    # location as (lat_float, lon_float, searchradius_string)
    # number of tweets to look at
    
    # is location is given, then use it for searching in radius
    if location != None:
        search_results = twitter.search(q = criterion, count = count, geocode = location)
        radius_str = location[-1]   # radius is stored as string in last element
        radius_nokm = re.findall('\d+', radius_str) # find only digits, remove km, returned as list
        radius = int(radius_nokm[0])    # therefore take this element
        if radius < 100:
            zoom = 6
        else:
            zoom = 3
    else:
        search_results = twitter.search(q=criterion, count=count)   # no location, just search
        zoom = 1        # zoom level maximum
    
    
    map_osm = folium.Map(location=[0, 0], zoom_start=zoom)  # center to origin
    
    
    ##parsing out 
    for tweet in search_results["statuses"]:
        tweet_text = tweet['text']
        coordinates = tweet['coordinates']
        if coordinates != None:
            actual_coordinates = coordinates['coordinates'] # coordinates are lat, lon
            actual_lon_lat = actual_coordinates.reverse() # for marker elements use lon, lat
            folium.Marker(actual_coordinates, popup = tweet_text).add_to(map_osm)   # set marker with tweet text
         
       
    map_osm.save(criterion+'.html')  # save map as criterion
    

locations_list = {'Amsterdam': [52.37403, 4.88969],
    'Wageningen': [51.97, 5.66667],
    'New York': [40.71427, -74.00597],
    'Berlin': [52.52437, 13.41053],
    }
    
loc = locations_list['Wageningen']
loc.append('100km')
if __name__ == '__main__':
    twitter_map_locations('traffic+jam', loc)
    twitter_map_locations('coffee', count = 5000)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# weather.py
# License: Public Domain
#
# Gets the weather and returns a string
# Why? Because I want a cute weather indicator in my prompt
# Requres: python-argparse

import argparse 
import urllib2
import json

def main():
    parser = argparse.ArgumentParser(description='Get the weather and return a string')
    parser.add_argument('-f', action="store_true", dest='fahrenheit', default=False,
                        help='Temp in Fahrenheit (default: False)')
    parser.add_argument('-z', action="store", dest="zipcode", default='10006',
                        help='your zipcode or your city name (default: NY)')
    parser.add_argument('-w', action="store_true", dest='show_wind', default=False,
                        help='Show wind speed')
    parser.add_argument('-H', action="store_true", dest='show_humidity', default=False,
                        help='Show relative humidity')
    parser.add_argument('-c', action="store_true", dest='show_city', default=False,
    			help='Show city name before weather data') 
    parser.add_argument('-t', action="store_true", dest='show_text', default=False,
    			help='Show condition description') 
     
    args = parser.parse_args()

    BASEURL = "http://api.wunderground.com/api/6c5f9a17518f02c6/"
    WURL = BASEURL + 'conditions/q/'
    geourl = BASEURL + "geolookup/q/%s.json" % (args.zipcode)

    try:
        f = urllib2.urlopen(geourl)
    except urllib2.HTTPError, urllib2.URLError:
        print "The URL is not reachable"
	return 1
    
    j = json.loads(str(f.read()))
    state = str(j['location']['state'])
    city = str(j['location']['city']).replace(' ','_')

    WURL += state + '/' + city + '.json'

    try:
        f = urllib2.urlopen(WURL)
    except urllib2.HTTPError, urllib2.URLError:
        print "The URL is not reachable"
	return 1
    
    j = json.loads(urllib2.urlopen(WURL).read())

    # Wunderground Full Weather dictionary
    wconditions = { 'Light Drizzle': "☂",
    	            'Heavy Drizzle': "☂",
    	            'Light Thunderstorm': "⚡",
    	            'Heavy Thunderstorm': "⚡",
                    'Light Rain': "☔",
                    'Heavy Rain': "☔",
                    'Chance of Rain': "☂",
                    'Light Rain Showers': "☔",
                    'Heavy Rain Showers': "☔",
                    'Light Thunderstorms and Rain': "⚡ ☔",
                    'Heavy Thunderstorms and Rain': "⚡ ☔",
    	            'Light Rain Mist': "☂",
    	            'Heavy Rain Mist': "☂",
    	            'Light Spray': "☂",
    	            'Heavy Spray': "☂",
                    'Light Snow': "☃",
                    'Heavy Snow': "☃",
                    'Light Snow Showers': "☃",
                    'Light Thunderstorms and Snow': "☃ ⚡",
                    'Heavy Thunderstorms and Snow': "☃ ⚡",
                    'Heavy Snow Showers': "☃",
                    'Light Blowing Snow': "☃",
                    'Heavy Blowing Snow': "☃",
                    'Light Low Drifting Snow': "☃",
                    'Heavy Low Drifting Snow': "☃",
                    'Light Snow Blowing Snow Mist': "☃",
                    'Heavy Snow Blowing Snow Mist': "☃",
                    'Light Snow Grains': "☃",
                    'Heavy Snow Grains': "☃",
                    'Light Ice Crystals': "☃",
                    'Heavy Ice Crystals': "☃",
                    'Light Ice Pellets': "☃",
                    'Heavy Ice Pellets': "☃",
                    'Light Ice Pellet Showers': "☃",
                    'Heavy Ice Pellet Showers': "☃",
		    'Light Freezing Drizzle': "☂ *",
		    'Heavy Freezing Drizzle': "☂ *",
		    'Light Freezing Rain': "☂ *",
		    'Heavy Freezing Rain': "☂ *",
    	            'Light Thunderstorms and Ice Pellets': "*⚡",
    	            'Heavy Thunderstorms and Ice Pellets': "*⚡",
                    'Light Hail': "*",
                    'Heavy Hail': "*",
                    'Small Hail': "*",
                    'Light Hail Showers': "*",
                    'Heavy Hail Showers': "*",
                    'Light Small Hail Showers': "*",
                    'Heavy Small Hail Showers': "*",
                    'Light Thunderstorms with Hail': "H⚡",
                    'Light Thunderstorms with Hail': "H⚡",
                    'Light Thunderstorms with Small Hail': "H⚡",
                    'Heavy Thunderstorms with Small Hail': "H⚡",
                    'Light Mist': "#",
                    'Heavy Mist': "#",
                    'Light Fog': "#",
                    'Heavy Fog': "#",
                    'Light Freezing Fog': "#☃",
                    'Heavy Freezing Fog': "#☃",
                    'Patches of Fog': "#",
                    'Shallow Fog': "#",
                    'Partial Fog': "#",
                    'Light Fog Patches': "#",
                    'Heavy Fog Patches': "#",
                    'Smoke': "S",
                    'Widespread Dust': "D",
                    'Light Blowing Widespread Dust': "D",
                    'Heavy Blowing Widespread Dust': "D",
                    'Light Low Drifting Widespread Dust': "D",
                    'Heavy Low Drifting Widespread Dust': "D",
                    'Light Dust Whirls': "D",
                    'Heavy Dust Whirls': "D",
                    'Light Sandstorm': "SS",
                    'Heavy Sandstorm': "SS",
                    'Light Sand': "SS",
                    'Heavy Sand': "SS",
                    'Light Blowing Sand': "SS",
                    'Heavy Blowing Sand': "SS",
                    'Light Low Drifting Sand': "SS",
                    'Heavy Low Drifting Sand': "SS",
    		    'Clear': "☉",
                    'Sunny': "☼",
                    'Mostly Sunny': "☼☁",
                    'Partly Cloudy': "☁ ☼",
                    'Mostly Cloudy': "☁",
                    'Scattered Clounds': "☁",
                    'Chance of Storm': "☁ ☂",
                    'Showers': "☂",
                    'Chance of Snow': "☃",
                    'Storm': "☈",
                    'Thunderstorm': "⚡",
                    'Chance of Storm': "☁?",
                    'Sleet': "S",
                    'Icy': "I",
                    'Light Haze': "H",
                    'Heavy Haze': "H",
                    'Flurries': "*",
                    'Overcast': "☁",
                    'Funnel Cloud': "Run!!!!",
                    'Squals': "SQ"}

    # prepare output
    weather = ""

    if args.show_city:
        weather += str(j['current_observation']['display_location']['city']) + " "

    if args.show_text:
    	weather += str(j['current_observation']['weather']) + " "
        
    if args.fahrenheit:
    	weather += str(j['current_observation']['temp_f']) + '°F '
    else:
        weather += str(j['current_observation']['temp_c']) + '°C '

    if args.show_wind:
    	weather += str(j['current_observation']['wind_dir']) + " " + str(j['current_observation']['wind_mph']) + " MPH "
    
    if args.show_humidity:
    	weather += str(j['current_observation']['relative_humidity']) + ' ϕ '


    # and now the end
    print wconditions[j['current_observation']['weather']] + '  ' + weather

    return 0

if __name__ == '__main__':
    main()


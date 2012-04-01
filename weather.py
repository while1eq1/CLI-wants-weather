#!/usr/bin/env python
# -*- coding: utf-8 -*-

# weather.py
# License: Public Domain
#
# Gets the weather and returns a string
# Why? Because I want a cute weather indicator in my prompt
# To Do? A lot of stuff
# Requres: python-argparse

import argparse 
import urllib2
from xml.dom.minidom import parse

def main():
    parser = argparse.ArgumentParser(description='Get the weather and return a string')
    parser.add_argument('-f', action="store_true", dest='fahrenheit', default=False,
                        help='Temp in Fahrenheit (default: False)')
    parser.add_argument('-z', action="store", dest="zipcode", default='NY',
                        help='your zipcode or your city name (default: NY)')
    
    args = parser.parse_args()

    WURL = "http://www.google.com/ig/api?weather="

    # fetching data
    req = urllib2.Request(WURL + args.zipcode)
    try:
        # Handling some URL and network Error
        f = urllib2.urlopen(req)
    except urllib2.HTTPError, urllib2.URLError:
        print 'The URL is not reachable'
        return 1
    dom = parse(f)

    # Weather dictionary
    # note that since google has not documented their API 
    # I could be missing some weather
    wconditions = { 'Drizzle': "☂",
    		    'Clear': "☉",
                    'Chance of Rain': "☂",
                    'Sunny': "☼",
                    'Mostly Sunny': "?",
                    'Partly Cloudy': "☁?",
                    'Mostly Cloudy': "☁☁",
                    'Chance of Storm': "☁☂",
                    'Showers': "☂",
                    'Rain': "☔",
                    'Chance of Snow': "☃",
                    'Cloudy': "☁",
                    'Mist': "#",
                    'Storm': "☈",
                    'Thunderstorm': "⚡",
                    'Chance of Storm': "☁?",
                    'Sleet': "S",
                    'Snow': "☃",
                    'Icy': "I",
                    'Dust': "D",
                    'Fog': "#",
                    'Smoke': "S",
                    'Haze': "H",
                    'Flurries': "*",
                    'Overcast': "☁"}

    # prepare output
    wsymbol = wconditions.get(dom.getElementsByTagName('condition')[0].getAttribute('data'))

    if args.fahrenheit:
        temp = dom.getElementsByTagName('temp_f')[0].getAttribute('data')
        unit = 'F'
    else:
        temp = dom.getElementsByTagName('temp_c')[0].getAttribute('data')
        unit = 'C'
        
    # and now the end
    print '%s %d°%s' % (wsymbol, int(temp), unit)

    return 0

if __name__ == '__main__':
    main()


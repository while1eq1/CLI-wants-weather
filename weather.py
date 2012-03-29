#!/usr/bin/python
# -*- coding: utf-8 -*-

# weather.py
# By: Lorenzo Bivens at gmail dot com 
# License: Public Domain
#
# Gets the weather and returns a string
# Why? Because I want a cute weather indicator in my prompt
# To Do? A lot of stuff

import urllib2
from xml.dom.minidom import parse

def main():
    # Look here if you need to configure something
    ZIPCODE = "limoges"
    WURL = "http://www.google.com/ig/api?weather="
    UNIT = 'C'

    # fetching data
    req = urllib2.Request(WURL + ZIPCODE)
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
    wconditions = { 'Clear': "☉",
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

    if UNIT == 'F':
        temp = dom.getElementsByTagName('temp_f')[0].getAttribute('data')
    else:
        temp = dom.getElementsByTagName('temp_c')[0].getAttribute('data')
        
    # and now the end
    print '%s %d°%s' % (wsymbol, int(temp), UNIT)

    return 0

if __name__ == '__main__':
    main()


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
    parser.add_argument('-w', action="store_true", dest='show_wind', default=False,
                        help='Show wind speed')
    parser.add_argument('-H', action="store_true", dest='show_humidity', default=False,
                        help='Show relative humidity')
    parser.add_argument('-c', action="store_true", dest='show_city', default=False,
    			help='Show city name before weather data') 
    parser.add_argument('-t', action="store_true", dest='show_text', default=False,
    			help='Show condition description') 
     
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
                    'Mostly Sunny': "☼☁",
                    'Partly Cloudy': "☁☼",
                    'Mostly Cloudy': "☁",
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
    
    weather = ""

    if args.show_city:
        weather += str(dom.getElementsByTagName('city')[0].getAttribute('data')) + " "

    if args.show_text:
    	weather += str(dom.getElementsByTagName('condition')[0].getAttribute('data')) + " "
        
    weather += str(wconditions.get(dom.getElementsByTagName('condition')[0].getAttribute('data'))) + " "

    if args.fahrenheit:
    	weather += str(dom.getElementsByTagName('temp_f')[0].getAttribute('data'))
        weather += '°F '
    else:
        weather += str(dom.getElementsByTagName('temp_c')[0].getAttribute('data'))
        weather += '°C '

    if args.show_wind:
    	weather += str(dom.getElementsByTagName('wind_condition')[0].getAttribute('data')).replace('Wind','≋') + " "
    
    if args.show_humidity:
    	weather += str(dom.getElementsByTagName('humidity')[0].getAttribute('data')).replace('Humidity','ϕ') 

        
    # and now the end
    # print '%s %d°%s' % (wsymbol, int(temp), unit)
    print weather

    return 0

if __name__ == '__main__':
    main()


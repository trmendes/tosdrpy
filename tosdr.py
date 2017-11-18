#!/usr/bin/env python

"""tosdr.py: This script will parse some info about a few service like facebook, google, amazon, etc."""

__author__      = "Thiago Mendes"
__copyright__   = "Creative Commons"
__credits__ = ["tosdr"]
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Thiago Mendes"
__email__ = "tribeirom@gmail.com"
__status__ = "Beta"
__link__ = 
import requests, re, sys

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def print_link_info(links, key):
    try:
        if (links[key]):
            print(links[key]['name'] + ": " + cleanhtml(links[key]['url']))
    except KeyError:
        pass

def show_links(links):
    print("\n\033[0;1m--== If you want to know more about it ==-- \033[0;0m\n")
    print_link_info(links, 'cookies');
    print_link_info(links, 'privacy');
    print_link_info(links, 'privacy-full');
    print_link_info(links, 'terms');
    print_link_info(links, 'definitions');
    print_link_info(links, 'faq');

def rating(value):
    print("\n\033[0;1m--== Rating for this service ==-- \033[0;0m\n")
    if (type(value) is str):
        if (value == 'A'):
            print("[CLASS A] They treat you fairly, respect your rights and will not abuse your data.")
        elif (value == 'B'):
            print("[CLASS B] The terms of services are fair towards the user but they could be improved.")
        elif (value == 'C'):
            print("[CLASS C] The terms of service are okay but some issues need your consideration.")
        elif (value == 'D'):
            print("[CLASS D] The terms of service are very uneven or there are some important issues that need your attention.")
        elif (value == 'E'):
            print("[CLASS E] The terms of service raise very serious concerns.")
    else:
        print("Tosdr haven't sufficiently reviewed the terms yet.")


def main():

    service = sys.argv[1]
    url = "https://tosdr.org/api/1/service/%s.json" % (service)

    print("\033[0;1m--== Terms of Service: Didn't Read ==-- \033[0;0m\n")
    print("...hold a second or more.... checking for " + service)

    r = requests.get(url)

    if (r.status_code == 200):
        json_dic = r.json()
        links = json_dic['links']
        ratingv = json_dic['class']

        print("\n\033[0;1m--== A few notes about it ==-- \033[0;0m\n")
        for x in range(0, len(json_dic['points'])):

            info = json_dic['pointsData'][json_dic['points'][x]]
            tosdr = info['tosdr']

            if (tosdr['point'] == "bad"):
                print('\033[0;31m- ' + info['title'] + '\033[0;0m')
            elif (tosdr['point'] == "neutral"):
                print('\033[0;33m- ' + info['title'] + '\033[0;0m')
            else:
                print('\033[0;32m- ' + info['title'] + '\033[0;0m')

            print(cleanhtml(tosdr['tldr']))

        rating(ratingv)
        show_links(links)

    else:
        print("\nOw $@#$%...I cant't find any information about " + service)
        print("anyway....")

    print("\n\033[0;1m--== Thanks to ==-- \033[0;0m\n")
    print("https://tosdr.org/")

if __name__ == "__main__":
    main()


#!/usr/bin/env python

"""tosdr.py: This script will parse some info about a few service like facebook, google, amazon, etc."""

__author__ = "Thiago Mendes"
__copyright__ = "Creative Commons"
__credits__ = ["tosdr"]
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Thiago Mendes"
__email__ = "tribeirom@gmail.com"
__status__ = "Beta"
__link__ = "https://gitlab.com/tmendes/tosdrpy"
import requests
import re
import argparse

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def print_link_info(links, key):
    try:
        if links[key]:
            print(links[key]['name'] + ": " + cleanhtml(links[key]['url']))
    except KeyError:
        pass


def show_links(links):
    print("\n\033[0;1m--== If you want to know more about it ==-- \033[0;0m\n")
    print_link_info(links, 'cookies')
    print_link_info(links, 'privacy')
    print_link_info(links, 'privacy-full')
    print_link_info(links, 'terms')
    print_link_info(links, 'definitions')
    print_link_info(links, 'faq')


def rating(value):
    print("\n\033[0;1m--== Rating for this service ==-- \033[0;0m\n")
    classes = { 'A': ' They treat you fairly, respect your rights and will not abuse your data.',
                'B': ' The terms of services are fair towards the user but they could be improved.',
                'C': ' The terms of service are okay but some issues need your consideration.',
                'D': ' The terms of service are very uneven or there are some important issues that need your attention.',
                'E': ' The terms of service raise very serious concerns.' }
    if isinstance(value, str):
            print("[CLASS " + value + classes[value])
    else:
        print("Tosdr haven't sufficiently reviewed the terms yet.")

def main():
    parser = argparse.ArgumentParser(description="making terms of service easier to read")
    parser.add_argument('--discussion', '-d', action='store_true', help='show links to the discussions')
    parser.add_argument('--simple', '-s', action='store_true', help='to print less info')
    parser.add_argument('service_name', type=str)
    args = parser.parse_args()

    url = "https://tosdr.org/api/1/service/%s.json" % (args.service_name)

    print("\033[0;1m--== Terms of Service: Didn't Read ==-- \033[0;0m\n")
    print("...hold a second or more.... checking for " + args.service_name)

    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(-1)

    if r.status_code == 200:
        data = r.json()
        links = data['links']
        ratingv = data['class']
        points_data = data['pointsData']
        points = data['points']
        score_colors = { "bad" : '\033[0;31m- ', "neutral" : '\033[0;33m- ', "good" : '\033[0;32m- '}

        print("\n\033[0;1m--== A few notes about it ==-- \033[0;0m\n")
        for idx in range(0, len(points)):

            info = points_data[points[idx]]
            tosdr = info['tosdr']

            print(score_colors[tosdr['point']] + info['title'] + '\033[0;0m')
            if args.simple is False:
                print(cleanhtml(tosdr['tldr']))
            if args.discussion:
                print("link: " + info['discussion'])

        rating(ratingv)
        if args.simple is False:
            show_links(links)

    else:
        print("\nOw $@#$%...I cant't find any information about " + service)
        print("anyway....")

    print("\n\033[0;1m--== Thanks to ==-- \033[0;0m\n")
    print("https://tosdr.org/")

if __name__ == "__main__":
    main()

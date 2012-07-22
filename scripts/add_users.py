#!/usr/bin/env python

import ConfigParser
import argparse
from redis import StrictRedis
from moodeque.models import (User, Venue)
import random

def parse_args():
    parser = argparse.ArgumentParser(description="Add venues")
    parser.add_argument("--ini", "-i", help="config ini file", required=True)
    parser.add_argument("--venue", "-v", type=int, help="Vanue name", required=True)
    parser.add_argument("--number", "-N", help="How many user to create",
                        type=int, default=100)
    args = parser.parse_args()
    return args

def parse_ini(ini):
    config = ConfigParser.ConfigParser()
    config.read(ini)

    return {k.replace("redis.", ""): v for k,v in config.items("app:main",
                                                               raw=True) if
            k.startswith("redis.")}


if __name__ == '__main__':
    args = parse_args()
    conf = parse_ini(args.ini)
    db = StrictRedis(**conf)
    venue = Venue.find(db, args.venue)

    print "Creating users: ",
    for i in xrange(args.number):
        username = "user{0}".format(i)
        mood = random.randrange(0, 10, 1)
        user = User.create(db, name=username, mood=mood)
        user.checkin(venue)
        print ".",

    print " Done."
    print venue.people

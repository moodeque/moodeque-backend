#!/usr/bin/env python

import ConfigParser
import argparse
from redis import StrictRedis
from moodeque.models import Venue

def parse_args():
    parser = argparse.ArgumentParser(description="Add venues")
    parser.add_argument("--ini", "-i", help="config ini file", required=True)
    parser.add_argument("--name", "-n", help="Vanue name", default=None)
    parser.add_argument("--description", "-d", help="Vanue description",
                        required=True)
    parser.add_argument("--latitude", "-l", help="Vanue latitude",
                        default=None)
    parser.add_argument("--longitude", "-L", help="Vanue longitude",
                        default=None)
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

    Venue.create(db, name=args.name, description=args.description,
                 latitude=args.latitude, longitude=args.longitude)


import time
import os
import argparse
import logging

def run():
    parser = argparse.ArgumentParser(description="sync_my_photos")
    parser.add_argument('-d', '--debug', action="store_true", default=False,
                        help="Enable debug")
    args = parser.parse_args()
    log = logging.getLogger()
    ch = logging.StreamHandler()
    log.addHandler(ch)

    if args.debug:
        print("Debug enabled")
        log.setLevel(logging.DEBUG)

    print("Syncing...")

run()

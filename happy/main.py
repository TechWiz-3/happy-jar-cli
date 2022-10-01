#!/usr/bin/env python3
# Happy jar cli, inspired by https://github.com/michelle/happy
# Created by Zac the Wise
# License: GPL-v3.0

from datetime import datetime
from sys import argv
from sys import exit
import argparse
import textwrap
import re

from happy.functions import read_file, write_file


def cli() -> None:
    description = "Log your good memories and gratitiude."
    epilog = "examples:\nhappy log \"i am so happy because you starred this project's repo on github xDD\"\nhappy get all\n\nFor more help use happy log --help and happy get --help"
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=description, epilog=textwrap.dedent(epilog)
    )

    subparsers = parser.add_subparsers(dest='command')

    log = subparsers.add_parser("log", help="logs an entry")
    log.add_argument("log_entry", help="log message in quotes")

    get = subparsers.add_parser("get", help="gets entries")
    get.add_argument("all", help="gets all entries", nargs="?")
    get.add_argument("today", help="gets today's entries", nargs="?")
    get.add_argument("before today", help="gets all entries before today", nargs="?")
    get.add_argument("random", help="gets a random entry", nargs="?")
    get.add_argument("random <number>", help="gets specified number of random entries", nargs="?")
    get.add_argument("<date>", help="gets a specified date's entries with dd/mm/yyyy", nargs="?")
    get.add_argument("after <date>", help="gets all entries after a date", nargs="?")
    get.add_argument("before <date>", help="gets all entries before a date", nargs="?")
    get.add_argument("--flowers", help="adds a random flower to your entry 🌼", action='store_true')

    args = parser.parse_args(argv[1:])

    if args.command == "log":
        write_file(args.log_entry)
        exit()
    if args.command == "get":

        # `happy get today`
        if args.all == "today":
            print("")
            read_file(today=True, flowers=args.flowers)
            exit()

        # `happy get all`
        elif args.all == "all":
            print("")
            read_file(flowers=args.flowers)

        # `happy get random [<num>]`
        elif args.all == "random":
            print("")
            if args.today:
                read_file(random=int(args.today), flowers=args.flowers)
            else:
                read_file(random=1, flowers=args.flowers)

        # `happy get [after|before|<date>]
        else:
            # checks for after or until command
            if args.all == "after" or args.all == "before":
                date = args.today
                # uses current date if input is today
                if args.today == "today":
                    date = datetime.now().strftime("%d/%m/%Y")
            else:
                date = args.all
            date_re = re.compile("^[0-9]{1,2}\/[0-9]{2}\/[0-9]{4}")
            print("")
            try:  # get the date provided
                dt = re.match(date_re, date)
            except TypeError:
                # this triggers the command
                # `happy get` without any other args
                print("Please use an argument after `get`\n")
                get.print_help()  # print usage for `get`
            else:
                if dt:
                    read_file(
                        date=dt.group(),
                        flowers=args.flowers,
                        after=args.all == "after",
                        before=args.all == "before"
                    )
            exit()

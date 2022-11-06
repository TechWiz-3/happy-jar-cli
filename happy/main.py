#!/usr/bin/env python3
# Happy jar cli, inspired by https://github.com/michelle/happy
# Created by Zac the Wise
# License: GPL-v3.0
import argparse
import re
import textwrap
from datetime import datetime
from sys import argv, exit

from rich.console import Console
from rich.markdown import Markdown

from happy.constants import THEME
from happy.functions import read_file, write_file

console = Console(highlight=False, theme=THEME)


def cli() -> None:
    description = "Log your good memories and gratitiude."
    epilog = 'examples:\nhappy log "i am so happy because you starred this project\'s repo on github xDD"\n`happy get all`\n\nFor more help use `happy log --help` and `happy get --help`'
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=description,
        epilog=textwrap.dedent(epilog),
    )

    subparsers = parser.add_subparsers(dest="command")

    log = subparsers.add_parser("log", help="logs an entry")
    log.add_argument("log_entry", help="log message in quotes")
    log.add_argument(
        "--tag <tag-without-spaces>", dest="tag", help="tags entry with specified tag", nargs="?"
    )

    get = subparsers.add_parser("get", help="gets entries")
    get.add_argument("all", help="gets all entries", nargs="?")
    get.add_argument("today", help="gets today's entries", nargs="?")
    get.add_argument("before today", help="gets all entries before today", nargs="?")
    get.add_argument("random", help="gets a random entry", nargs="?")
    get.add_argument(
        "random <number>", help="gets specified number of random entries", nargs="?"
    )
    get.add_argument(
        "<date>", help="gets a specified date's entries with dd/mm/yyyy", nargs="?"
    )
    get.add_argument(
        "count", help="displays how many times you were happy each day", nargs="?"
    )
    get.add_argument(
        "tags", help="displays a list of all the tags used so far", nargs="?"
    )
    get.add_argument("after <date>", help="gets all entries after a date", nargs="?")
    get.add_argument("before <date>", help="gets all entries before a date", nargs="?")
    get.add_argument(
        "tag <tag-without-spaces>", help="gets only entries with specified tag", nargs="?"
    )
    get.add_argument(
        "--flowers", help="adds a random flower to your entry 🌼", action="store_true"
    )
    get.add_argument(
        "--nocolor",
        help="displays entries without any color formatting",
        action="store_true",
    )

    args = parser.parse_args(argv[1:])

    if args.command == "log":
        write_file(args.log_entry, args.tag)
        exit()

    if args.command == "get":

        def header(msg=""):
            console.rule(f"[bold]{msg}", style="bold color(105)", align="left")
            console.print("")

        footer = header

        if args.all == "tag" and args.today:
            tag = args.today
            console.print("")
            header("Entries tagged with " + tag)
            read_file(tag=tag, flowers=args.flowers, nocolor=args.nocolor)
            footer()

        # `happy get today`
        elif args.all == "today":
            console.print("")
            header("Today's Entries")
            read_file(today=True, flowers=args.flowers, nocolor=args.nocolor)
            footer()
            exit()

        # `happy get all`
        elif args.all == "all":
            console.print("")
            header("All Entries")
            read_file(flowers=args.flowers, nocolor=args.nocolor)
            footer()

        # `happy get random [<num>]`
        elif args.all == "random":
            console.print("")
            if args.today:
                try:
                    random_num = int(args.today)
                    header("Random Entries")
                    read_file(
                        random=random_num, flowers=args.flowers, nocolor=args.nocolor
                    )
                except ValueError:  # a valid number wasn't provided
                    console.print(
                        Markdown("Error: please enter a valid number after `random` or `random` on it's own"),
                        style="error",)
                    print("")
                    exit()
            else:
                header("Random Entry")
                read_file(random=1, flowers=args.flowers, nocolor=args.nocolor)
            footer()

        # `happy get count`
        elif args.all == "count":
            console.print("")
            header("Happyjar count")
            read_file(count=True, flowers=args.flowers, nocolor=args.nocolor)
            footer()

        # `happy get tags`
        elif args.all == "tags":
            console.print("")
            header("Tags")
            read_file(tags=True, flowers=args.flowers, nocolor=args.nocolor)
            footer()

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
            console.print("")
            try:  # get the date provided
                dt = re.match(date_re, date)
            except TypeError:
                # this triggers with the command
                # `happy get` without any other args
                console.print("Please use an argument after `get`\n", style="warning")
                get.print_help()  # print usage for `get`
            else:
                if dt:
                    if args.all == "before" or args.all == "after":
                        header(f"Entries logged {args.all} {dt.group()}")
                    else:
                        header(f"Entries logged on {dt.group()}")
                    read_file(
                        date=dt.group(),
                        flowers=args.flowers,
                        after=args.all == "after",
                        before=args.all == "before",
                        nocolor=args.nocolor,
                    )
                    footer()
                else:
                    console.print(
                        Markdown("Error: incorrect usage! If you are entering a date, use the format `dd/mm/yyyy`\n"),
                        style="error",
                    )
                    get.print_help()  # print usage for `get`

            exit()


if __name__ == "__main__":
    cli()

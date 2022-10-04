#!/usr/bin/env python3
# Happy jar cli, inspired by https://github.com/michelle/happy
# Created by Zac the Wise
# License: GPL-v3.0

from datetime import datetime
from os.path import expanduser
from sys import argv
from os.path import exists
from sys import exit
from random import choice, sample
import argparse
import textwrap
import re

HOME = expanduser("~")


def write_file(payload, time=None):
    if time is None:
        time = datetime.today()
        try:
            time = time.strftime("%A %-d/%b/%Y %-I:%M %p")
        except ValueError:
            time = time.strftime("%A %d/%b/%Y %I:%M %p")

    if exists(f"{HOME}/.happyjar.txt"):
        try:
            with open(f"{HOME}/.happyjar.txt", "a") as happy_file:
                happy_file.write(f"{time}: {payload}\n")
        except Exception as err:
            print(f"Error occurred: {err}")
        else:
            print("Entry written successfully!")
    else:
        try:
            with open(f"{HOME}/.happyjar.txt", "w") as happy_file:
                happy_file.write(f"{time}: {payload}\n")
        except Exception as err:
            print(f"Error occurred: {err}")
        else:
            print(
                "\nJar created!\nEntry written successfully!\nUse 'happy get all' or 'happy get today' to view your logs!"
            )


def read_file(
    date=False, today=False, flowers=False, after=False, before=False, random=0
):
    if not exists(f"{HOME}/.happyjar.txt"):
        print(
            "Error: your happyjar has not been initialised yet. To do that, log an entry using 'happy log \"my first log\"'.\nFor more info use 'happy log -h'\n"
        )
        exit()

    if today:
        time = datetime.today()
        try:
            today = time.strftime("%A %-d/%b/%Y")
        except ValueError:
            today = time.strftime("%A %d/%b/%Y")
        dt_re = re.compile(f"^{today}")

        with open(f"{HOME}/.happyjar.txt", "r") as happy_file:
            for line in happy_file:
                if dt_re.match(line):
                    display_entry(flowers, line)

    elif date:
        try:  # convert user inputted string to dt object
            converted_dt = datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            print("Error: please enter the date as the format dd/mm/yyyy")
            exit()
        else:
            try:
                # format dt object
                formatted_dt = datetime.strftime(converted_dt, "%A %-d/%b/%Y")
            except ValueError:
                # format dt object
                formatted_dt = datetime.strftime(converted_dt, "%A %d/%b/%Y")

            dt_re = re.compile(f"^{formatted_dt}")
            with open(f"{HOME}/.happyjar.txt") as happy_file:
                for line in happy_file:
                    if line != "\n":
                        # get the date of the line
                        date = line.split()[1]
                        dt = datetime.strptime(date, "%d/%b/%Y")
                        if after:
                            if dt > converted_dt:
                                display_entry(flowers, line)
                        elif before:
                            if dt < converted_dt:
                                display_entry(flowers, line)
                            else:
                                break
                        else:
                            match = re.match(dt_re, line)
                            if match:
                                display_entry(flowers, line)

    elif random:  # get a random entry
        with open(f"{HOME}/.happyjar.txt") as happy_file:
            lines = happy_file.readlines()
            for line in sample(lines, min(random, len(lines))):
                display_entry(flowers, line)

    elif not date and not today:  # assume the whole file should be printed
        with open(f"{HOME}/.happyjar.txt", "r") as happy_file:
            for line in happy_file:
                display_entry(flowers, line)


def display_entry(flowers, line):
    """displays entries with or without flowers"""
    flower = ""
    flower_selection = ["🌼 ", "🍀 ", "🌻 ", "🌺 ", "🌹 ", "🌸 ", "🌷 ", "💐 ", "🏵️  "]
    if line != "\n" and flowers:
        flower = choice(flower_selection)
        print(f"{flower}{line}")
    else:
        print(line)


def cli() -> None:
    description = "Log your good memories and gratitiude."
    epilog = "examples:\nhappy log \"i am so happy because you starred this project's repo on github xDD\"\n'happy get all'\n\nFor more help use 'happy log --help' and 'happy get --help'"
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=description,
        epilog=textwrap.dedent(epilog),
    )

    subparsers = parser.add_subparsers(dest="command")

    log = subparsers.add_parser("log", help="logs an entry")
    log.add_argument("log_entry", help="log message in quotes")

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
    get.add_argument("after <date>", help="gets all entries after a date", nargs="?")
    get.add_argument("before <date>", help="gets all entries before a date", nargs="?")
    get.add_argument(
        "--flowers", help="adds a random flower to your entry 🌼", action="store_true"
    )

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
                print("Please use an arguement after `get`\n")
                get.print_help()  # print usage for `get`
            else:
                if dt:
                    read_file(
                        date=dt.group(),
                        flowers=args.flowers,
                        after=args.all == "after",
                        before=args.all == "before",
                    )
            exit()


if __name__ == "__main__":
    cli()

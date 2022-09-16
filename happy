#!/usr/bin/env python3
# Happy jar cli, inspired by https://github.com/michelle/happy
# Created by Zac the Wise
# License: GPL-v3.0

# Todo
# Get until date
# Get before data

from datetime import datetime
from os.path import expanduser
from sys import argv
from os.path import exists
from random import choice
import argparse
import textwrap
import re

HOME = expanduser("~")

def write_file(payload, time=None):

    if time == None:
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
            print("Jar created!")
            print("Entry written successfully!")
            print("Use happy get all or happy get today to view your logs!")

def read_file(date=False, today=False, flowers=False):
    flower = ""
    flower_selection = ["🌼 ", "🍀 ", "🌻 ", "🌺 ", "🌹 ", "🌸 ", "🌷 ", "💐 ", "🏵️  "]

    if not exists(f"{HOME}/.happyjar.txt"):
        print("Error: your happyjar has not been initialised yet. To do that, log an entry using happy log \"my first log\".\nFor more info use happy log -h\n")
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
                    if flowers:
                        flower = choice(flower_selection)
                    print(f"{flower}{line}")

    elif date:
        try:  # convert user inputted string to dt object
            converted_dt = datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            print("Error: please enter the date as the format dd/mm/yyyy")
            exit()
        else:
            try:
                converted_dt = datetime.strftime(converted_dt, "%A %-d/%b/%Y")  # format dt object
            except ValueError:
                converted_dt = datetime.strftime(converted_dt, "%A %d/%b/%Y")  # format dt object
            dt_re =  re.compile(f"^{converted_dt}")
            with open(f"{HOME}/.happyjar.txt") as happy_file:
                for line in happy_file:
                    if line != "\n":
                        match = re.match(dt_re,line)
                        if match:
                            if match.group():
                                if flowers:
                                    flower = choice(flower_selection)
                                print(f"{flower}{line}")


    elif not date and not today:  # assume the whole file should be printed
        with open(f"{HOME}/.happyjar.txt", "r") as happy_file:
            for line in happy_file:
                if line != "\n" and flowers == True:
                    flower = choice(flower_selection)
                    print(f"{flower}{line}")
                else:
                    print(line)

if __name__ == "__main__":

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
    get.add_argument("date", help="gets a specified date's entries with dd/mm/yyyy", nargs="?")
    get.add_argument("--flowers", help="adds a random flower to your entry 🌼", action='store_true')

    args = parser.parse_args(argv[1:])

    if args.command == "log":
        write_file(args.log_entry)
        exit()
    if args.command == "get":
        if args.all == "today":
            print("")
            read_file(today=True, flowers=args.flowers)
            exit()
        elif args.all == "all":
            print("")
            read_file(flowers=args.flowers)
        else:
            date_re = re.compile("^[0-9]{1,2}\/[0-9]{2}\/[0-9]{4}")
            print("")
            try:
                dt = re.match(date_re, args.all)
            except TypeError:
                read_file(flowers=args.flowers)
            else:
                if dt:
                    read_file(date=dt.group(), flowers=args.flowers)
            exit()

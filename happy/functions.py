from datetime import datetime
from os.path import exists
from sys import exit
from random import choice, sample
import re

from happy.constants import HOME, FLOWERS


def write_file(payload, time=None):
    """Writes entry to happy jar"""
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
            print("Jar created!")
            print("Entry written successfully!")
            print("Use happy get all or happy get today to view your logs!")


def read_file(
    date=False, today=False,
    flowers=False, after=False,
    before=False, random=0
):
    """Reads entries from happy jar"""
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
    """Display a happy jar entry with or without flowers"""
    if line != "\n" and flowers:
        flower = choice(FLOWERS)
        print(f"{flower}{line}")
    else:
        print(line)

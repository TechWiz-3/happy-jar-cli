import json
import os
from datetime import datetime, timedelta
from random import choice, sample
from sys import exit

from rich.console import Console
from rich.markdown import Markdown


from happy.constants import DATA_PATH, OLD_DATA_PATH
from happy.constants import THEME

console = Console(highlight=False, theme=THEME)

# stores the last flower used so
# it can be skipped
skip_flower = ""


def write_file(entry, tag, time=None):
    """
    logs are stored in a 'logs' array
    the logs array contains an object for each log
    each object contains the following
    day: day of the week
    date: dd/mm/yyyy
    time: h:mm AM/PM
    message: the actual log
    tags: array of tags
    """

    file_init = {"logs": []}  # initial state of .happyjar.json

    if tag:  # check if --tag was used
        # add the tag to the entry text
        entry = entry + " #" + tag
        # the tag will be unpacked from the entry later
    if not time:  # check if user did not specify time
        time = datetime.today()
        # format datetime to be
        # day&date&time
        try:
            time_str = time.strftime("%A&%-d/%b/%Y&%-I:%M %p")
        except ValueError:
            time_str = time.strftime("%A&%d/%b/%Y&%I:%M %p")
        # unpack datetime
        day, date, clock_time = time_str.split('&')

        # get tags passed into the message
        message, *tags = entry.split(" #")
        print(message, tags, *tags)

        payload = {"day": day, "date": date, "time": clock_time, "message": message, "tags": tags}

    if os.path.exists(DATA_PATH):  # checks for an existing .json data_file
        try:
            with open(DATA_PATH, "+r") as happy_file:
                happy_data = json.load(happy_file)
                happy_data["logs"].append(payload)
                happy_file.seek(0)
                json.dump(happy_data, happy_file, indent=4)

        except Exception as err:
            console.print(f"Error occurred: {err}", style="error")
        else:
            console.print("\nEntry written successfully!\n", style="info")
    else:  # migrate happyjar.txt to happyjar.json
        try:
            with open(DATA_PATH, "w") as happy_file:
                old_payload = []
                if os.path.exists(OLD_DATA_PATH):  # check if user has the old .txt file
                    with open(OLD_DATA_PATH, 'r') as old_file:
                        for line in old_file:
                            line = line[:-1].split(": ")
                            day, date, *time = line[0].split()
                            time = ' '.join(time)
                            message, *tags = line[1].split(" #")
                            old_payload.append({"day": day, "date": date, "time": time, "message": message, "tags": tags})
                file_init["logs"].extend(old_payload)  # add data from .txt to the .json file first
                file_init["logs"].append(payload)
                json.dump(file_init, happy_file, indent=4)

        except Exception as err:
            console.print(f"Error occurred: {err}", style="error")
        else:
            console.print("\nJar created!\nEntry written successfully!\n", Markdown("Use `happy get all` or `happy get today` to view your logs!"), "", style="info")


def display_entry(flowers, log, nocolor, string=False):
    """
    displays entries with or without flowers
    ---
    flowers: is set to True or False
    log: entry object as a dict with date, day, tags and log
    nocolor: specifies entry output should be formatted with color
    string: specifies if the log is in string form which requires direct output
    """

    global skip_flower  # the last flower used
    flower_selection = ["🌼 ", "🍀 ", "🌻 ", "🌺 ", "🌹 ", "🌸 ", "🌷 ", "💐 ", "🏵️  "]

    if flowers:
        # randomly choose any flower except skip_flower to avoid repetition
        flower = choice([item for item in flower_selection if item != skip_flower])
        skip_flower = flower
    else:
        flower = ""

    # display the output directly strings
    if string:
        console.print(f"{flower}{log}")
        return

    # extract data from log
    date = f"{log['day']} {log['date']} {log['time']}"
    entry = log['message']
    tags = " ".join(f"#{tag}" for tag in log['tags'])

    # toggle whether to display colors or not
    toggle_style = ["date", "message", "tags"]
    if nocolor:
        toggle_style = ["default", "default", "default"]

    # print line
    console.print(f"{flower}[{toggle_style[0]}][{date}][/{toggle_style[0]}]: [{toggle_style[1]}]{entry}[/{toggle_style[1]}] [{toggle_style[2]}]{tags}[/{toggle_style[2]}]\n")


def read_file(
    tag=None,
    date=False,
    today=False,
    lastndays=False,
    days=0,
    flowers=False,
    after=False,
    before=False,
    random=0,
    count=False,
    tags=False,
    nocolor=False,
):
    display = False
    if not os.path.exists(DATA_PATH):
        console.print("Error: your happyjar has not been initialised yet.",
                      Markdown("To initialise your happyjar, log an entry using `happy log <YOUR_ENTRY>`."), "",
                      Markdown("For more info use `happy log -h`"), "", style="error")
        exit()

    if today:
        time = datetime.today()
        try:
            today = time.strftime("%A %-d/%b/%Y")
        except ValueError:
            today = time.strftime("%A %d/%b/%Y")

        with open(DATA_PATH, "r") as happy_file:
            happy_data = json.load(happy_file)  # converts json file to dictionary
            for log in happy_data['logs']:
                if f"{log['day']} {log['date']}" == today:
                    display = True
                    display_entry(flowers, log, nocolor)

    if lastndays:
        inital_time = datetime.today() - timedelta(days=days)

        with open(DATA_PATH, "r") as happy_file:
            happy_data = json.load(happy_file)  # converts json file to dictionary
            for log in happy_data['logs']:
                date = log['date']
                dt = datetime.strptime(date, "%d/%b/%Y")
                if dt > inital_time:
                    display = True
                    display_entry(flowers, log, nocolor)

    elif tag is not None:
        with open(DATA_PATH, "r") as happy_file:
            happy_data = json.load(happy_file)
            for log in happy_data['logs']:
                if tag in log['tags']:
                    display = True
                    display_entry(flowers, log, nocolor)

    elif date:
        try:  # convert user inputted string to dt object
            converted_dt = datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            console.print("Error occurred converting date to date object", style="error")
            exit()
        else:
            try:
                # format dt object
                formatted_dt = datetime.strftime(converted_dt, "%-d/%b/%Y")
            except ValueError:
                # format dt object
                formatted_dt = datetime.strftime(converted_dt, "%d/%b/%Y")

            with open(DATA_PATH) as happy_file:
                happy_data = json.load(happy_file)
                for log in happy_data['logs']:
                    # get the date of the line
                    date = log['date']
                    dt = datetime.strptime(date, "%d/%b/%Y")
                    if after:  # `happy get after <date>`
                        if dt > converted_dt:
                            display = True
                            display_entry(flowers, log, nocolor)
                    elif before:  # `happy get before <date>`
                        if dt < converted_dt:
                            display = True
                            display_entry(flowers, log, nocolor)
                        else:
                            break
                    else:  # `happy get <date>`
                        if date == formatted_dt:
                            display = True
                            display_entry(flowers, log, nocolor)

    elif random:  # get a random entry
        with open(DATA_PATH) as happy_file:
            happy_data = json.load(happy_file)
            logs = happy_data['logs']
            for log in sample(logs, min(random, len(logs))):
                display = True
                display_entry(flowers, log, nocolor)

    elif count:  # get count of all entries per day
        map = {}  # map to store the count of entries
        with open(DATA_PATH, "r") as happy_file:
            happy_data = json.load(happy_file)
            for log in happy_data['logs']:
                key = log['date']
                # if the date hasn't already been added
                if key not in map.keys():
                    map[key] = 1
                else:  # if date has been added
                    map[key] += 1  # increment count
        for item in map:
            count = "" if map[item] == 1 else "s"  # time/s
            output = f"You were happy {map[item]} time{count} on {item}\n"
            display = True
            display_entry(flowers, output, nocolor, string=True)

    elif tags:
        tags_list = []
        with open(DATA_PATH, "r") as happy_file:
            happy_data = json.load(happy_file)
            for log in happy_data['logs']:
                tags_list.extend(log['tags'])
        tags_list = list(dict.fromkeys(tags_list))  # removing duplicates
        display = True
        tag_count = len(tags_list)
        if tag_count == 0:
            console.print("You have not used any tags so far", style="warning")
        elif tag_count == 1:
            console.print("You have used 1 tag so far")
            display_entry(flowers, f"{tags_list[0]}", nocolor, tags=True)
        else:
            console.print(f"You have used {tag_count} tags so far:")
            for tag in tags_list:
                display_entry(flowers, tag, nocolor, string=True)
        console.print("")

    else:  # assume the whole file should be printed
        with open(DATA_PATH, "r") as happy_file:
            happy_data = json.load(happy_file)
            for log in happy_data['logs']:
                display = True
                display_entry(flowers, log, nocolor)
    if not display:  # triggers if nothing was printed
        console.print("No entries for selected tag or time period\n", style="info")

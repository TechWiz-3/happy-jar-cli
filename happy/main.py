#!/usr/bin/env python3
# Happy jar cli, inspired by https://github.com/michelle/happy
# Created by Zac the Wise
# License: GPL-v3.0
import re
import os.path
import argparse
import textwrap
from datetime import datetime
from sys import argv, exit
from random import choice, sample
from rich.console import Console
from rich.markdown import Markdown
from rich.theme import Theme

custom_theme = Theme(
    {
        "info": "bold color(39)",
        "error": "bold red",
        "date": "color(111)",
        "entry": "default",
        "warning": "italic dim yellow",
    }
)

DATA_PATH = os.path.join(os.getenv("HOME"), ".happyjar.json")

console = Console(highlight=False, theme=custom_theme)

# stores the last flower used so
# it can be skipped
skip_flower = ""


def write_file(payload, tag, time=None):
    if tag is not None:
        payload = payload + " #" + tag
    if time is None:
        time = datetime.today()
        try:
            time = time.strftime("%A %-d/%b/%Y %-I:%M %p")
        except ValueError:
            time = time.strftime("%A %d/%b/%Y %I:%M %p")

    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, "a") as happy_file:
                happy_file.write(f"{time}: {payload}\n")
        except Exception as err:
            console.print(f"Error occurred: {err}", style="error")
        else:
            console.print("\nEntry written successfully!\n", style="info")
    else:
        try:
            with open(DATA_PATH, "w") as happy_file:
                happy_file.write(f"{time}: {payload}\n")
        except Exception as err:
            console.print(f"Error occurred: {err}", style="error")
        else:
            console.print(
                "\nJar created!\nEntry written successfully!\n",
                Markdown("Use `happy get all` or `happy get today` to view your logs!"),
                "",
                style="info",
            )


def read_file(
    tag=None,
    date=False,
    today=False,
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
        console.print(
            "Error: your happyjar has not been initialised yet.",
            Markdown(
                "To initialise your happyjar, log an entry using `happy log <YOUR_ENTRY>`."
            ),
            "",
            Markdown("For more info use `happy log -h`"),
            "",
            style="error",
        )
        exit()

    if today:
        time = datetime.today()
        try:
            today = time.strftime("%A %-d/%b/%Y")
        except ValueError:
            today = time.strftime("%A %d/%b/%Y")
        dt_re = re.compile(f"^{today}")

        with open(DATA_PATH, "r") as happy_file:
            for line in happy_file:
                if dt_re.match(line):
                    display = True
                    display_entry(flowers, line, nocolor)

    elif tag is not None:
        with open(DATA_PATH, "r") as happy_file:
            for line in happy_file:
                if line.strip().endswith(" #" + tag):
                    display = True
                    display_entry(flowers, line, nocolor)

    elif date:
        try:  # convert user inputted string to dt object
            converted_dt = datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            console.print(
                "Error occurred converting date to date object", style="error"
            )
            exit()
        else:
            try:
                # format dt object
                formatted_dt = datetime.strftime(converted_dt, "%A %-d/%b/%Y")
            except ValueError:
                # format dt object
                formatted_dt = datetime.strftime(converted_dt, "%A %d/%b/%Y")

            dt_re = re.compile(f"^{formatted_dt}")
            with open(DATA_PATH) as happy_file:
                for line in happy_file:
                    if line != "\n":
                        # get the date of the line
                        date = line.split()[1]
                        dt = datetime.strptime(date, "%d/%b/%Y")
                        if after:  # `happy get after <date>`
                            if dt > converted_dt:
                                display = True
                                display_entry(flowers, line, nocolor)
                        elif before:  # `happy get before <date>`
                            if dt < converted_dt:
                                display = True
                                display_entry(flowers, line, nocolor)
                            else:
                                break
                        else:  # `happy get <date>`
                            match = re.match(dt_re, line)
                            if match:
                                display = True
                                display_entry(flowers, line, nocolor)

    elif random:  # get a random entry
        with open(DATA_PATH) as happy_file:
            lines = happy_file.readlines()
            for line in sample(lines, min(random, len(lines))):
                display = True
                display_entry(flowers, line, nocolor)

    elif count:  # get count of all entries per day
        map = {}  # map to store the count of entries
        with open(DATA_PATH, "r") as happy_file:
            for line in happy_file:
                key = line.split()
                # if the date hasn't already been added
                if key[1] not in map.keys():
                    map[key[1]] = 1
                else:  # if date has been added
                    map[key[1]] += 1  # increment count
        for item in map:
            count = "" if map[item] == 1 else "s"  # time/s
            output = f"You were happy {map[item]} time{count} on {item}"
            display = True
            display_entry(flowers, output, nocolor, count=True)
        print("")

    elif tags:
        tags_list = []
        with open(DATA_PATH, "r") as happy_file:
            for line in happy_file:
                last_word = line.split()[-1]
                if last_word.startswith("#"):
                    tags_list.append(last_word[1:])
        tags_list = list(dict.fromkeys(tags_list))  # removing duplicates
        display = True
        tag_count = len(tags_list)
        if tag_count == 0:
            console.print("You have not used any tags so far", style="warning")
        elif tag_count == 1:
            print("You have used 1 tag so far")
            display_entry(flowers, f"{tags_list[0]}", nocolor, tags=True)
        else:
            print(f"You have used {tag_count} tags so far:")
            for tag in tags_list:
                display_entry(flowers, tag, nocolor, tags=True)
        print("")

    else:  # assume the whole file should be printed
        with open(DATA_PATH, "r") as happy_file:
            for line in happy_file:
                display = True
                display_entry(flowers, line, nocolor)
    if not display:  # triggers if nothing was printed
        console.print("No entries for selected tag or time period\n", style="info")


def display_entry(flowers, line, nocolor, count=False, tags=False):
    """
    displays entries with or without flowers
    ---
    flowers: is set to True or False
    line: is the entry that should be printed
    """
    global skip_flower  # the last flower used
    flower = ""
    flower_selection = ["🌼 ", "🍀 ", "🌻 ", "🌺 ", "🌹 ", "🌸 ", "🌷 ", "💐 ", "🏵️  "]

    if not count and not tags:
        # format the output
        line = line.split(": ")
        date = line[0]
        entry = line[1]
        toggle_style = ["date", "entry"]
    if nocolor:
        toggle_style = ["default", "default"]

    if count or tags:
        flower = choice(flower_selection)
        # randomly choose any flower except skip_flower to avoid repetition
        flower = choice([item for item in flower_selection if item != skip_flower])
        skip_flower = flower

        if flowers:
            console.print(f"\n{flower}{line}")
        else:
            console.print(line)
            if count:
                print("")  # print extra newline
        return

    # print line
    if line != "\n" and flowers:
        flower = choice(flower_selection)
        # randomly choose any flower except skip_flower to avoid repetition
        flower = choice([item for item in flower_selection if item != skip_flower])
        skip_flower = flower
        console.print(
            f"{flower} [{toggle_style[0]}][{date}][/{toggle_style[0]}]: [{toggle_style[1]}]{entry}[/{toggle_style[1]}]"
        )
    else:  # regular, no flowers entry printing
        console.print(
            f"[{toggle_style[0]}][{date}][/{toggle_style[0]}]: [{toggle_style[1]}]{entry}[/{toggle_style[1]}]"
        )


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
                        Markdown(
                            "Error: please enter a valid number after `random` or `random` on it's own"
                        ),
                        style="error",)
                    print("")
                    exit()
            else:
                header("Random Entry")
                read_file(random=1, flowers=args.flowers, nocolor=args.nocolor)
            footer()

        # `happy get count`
        elif args.all == "count":
            print("")
            read_file(count=True, flowers=args.flowers, nocolor=args.nocolor)

        # `happy get tags`
        elif args.all == "tags":
            print("")
            read_file(tags=True, flowers=args.flowers, nocolor=args.nocolor)

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
                        Markdown(
                            "Error: incorrect usage! If you are entering a date, use the format `dd/mm/yyyy`\n"
                        ),
                        style="error",
                    )
                    get.print_help()  # print usage for `get`

            exit()


if __name__ == "__main__":
    cli()

# Parse arguements and options and return keywords indicating what commands to
# execute


def args(args):
    # the args recieved include the command invokation
    if len(args) == 1:
        return "error", "you need to include a happy note or arguements, please refer to happy --helo"
    if "-" in args[1] or "--" in args[1]:  # options being used
        if args[1] in ("-a" "--all"):
            return "show all", None
        if args[1] in ("-h", "--help"):
            return "help", None
        # if the option isn't recognised as above
        return "error", "unrecognised usage, please refer to happy --help"
    else:
        payload = args[1:]
        return "write", payload

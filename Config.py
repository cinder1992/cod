#!/usr/bin/python

from src.cod import VERSION
from src.niilib.config import Config

import json

config = Config("etc/config.json.example").config

def promptUser(prompt, default):
    inp = raw_input("%s [%s]> " % (prompt, default))

    if inp == "":
        return default
    else:
        return inp

def limitReplies(prompt, default, valid):
    inp = ""

    while inp not in valid:
        if inp != "":
            print "Sorry, %s is not a valid choice. Valid choices are:" % inp

            for entry in valid:
                print " - %s" % entry

        inp = promptUser(prompt, default)

    return inp

art = """  ____          _
 / ___|___   __| |
| |   / _ \ / _` |
| |__| (_) | (_| |
 \____\___/ \__,_| version %s""" % VERSION

print art
print "Configuration script\n"

ircd = limitReplies("What irc daemon are you using?", "elemental-ircd",
        ["elemental-ircd", "charybdis", "inspircd"])

sname = promptUser("What server name do you want to use?", "cod.int")

netname = promptUser("What network are you deploying this to?", "ExampleNET")

prefix = promptUser("What command prefix would you like to use?", "@")

snoopchan = promptUser("What is your services snoop channel?", "#services")
staffchan = promptUser("What is your staff channel?", "#opers")
helpchan = promptUser("What is your help channel?", "#help")

contrib = limitReplies("Do you want to use contrib modules? [Y/N]", "N", ["Y", "N"]) == "Y"

config["uplink"]["protocol"] = ircd
config["me"]["netname"] = netname
config["me"]["name"] = sname
config["me"]["prefix"] = prefix
config["etc"]["snoopchan"] = snoopchan
config["etc"]["staffchan"] = staffchan
config["etc"]["helpchan"] = helpchan
config["etc"]["contrib"] = contrib

conf = json.dumps(config, sort_keys=True, indent=4, separators=(',', ': '))

with open("config.json", "w") as fout:
    fout.write(conf)

print art
print "\nYour config file has been written to config.json. You should now open it"
print "in a text editor and finish filling in things like the link password.\n"

print "Thank you for using Cod, visit us online at https://github.com/cod-services/cod"


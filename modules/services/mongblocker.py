"""
<Zlib text>
"""

NAME="Mong Blocker"
DESC="Filters spam from errant users by kicks and bans"

from utils import *

global client
global channels

def initModule(cod):
    global client

    client = makeService("MongBlocker", "hammer", "thors.grace", "Mong Blocker", cod.getUID())

    cod.s2scommands["PRIVMSG"].append(handleMessages)

    cod.clients[client.uid] = client

    cod.sendLine(client.burst())

    cod.log("Bursting MongBlocker client", "!!!")

    initDBTable(cod, "MBAutojoin", "Id INTEGER PRIMARY KEY, Name TEXT")
    initDBTable(cod, "Chances",
            "Id INTEGER PRIMARY KEY, Uid TEXT, Channel TEXT, Chances INTEGER")

    cod.sendLine(client.join(cod.channels[cod.config["etc"]["snoopchan"]]))

def destroyModule(cod):
    global client

    cod.s2scommands["PRIVMSG"].remove(handleMessages)

    cod.sendLine(client.quit())

    deletefromDB(cod, "DROP TABLE Chances")

    cod.clients.pop(client.uid)

def handleMessages(cod, line, splitline, source):
    global client
    global channels

    pm = splitline[2] == client.uid

    line = ":".join(line.split(":")[2:])
    splitline = line.split()

    #Do I care?
    if spltline[2] not in channels:
        return

    if cod.clients[source].isOper:
        if pm:
            if splitline[0].upper() == "JOIN":
                if splitline[1][0] == "#":
                    channel = splitline[1]

                    if splitline[1] not in cod.channels:
                        cod.notice(source, "I don't know about %s" % channel, client)
                        return

                    cod.join(channel, client)

                    admclient = cod.clients[source]
                    cod.servicesLog("JOIN %s: %s" % (channel, admclient.nick))
                    cod.notice(source, "I am monitoring $s" % channel)

                    

                    addtoDB(cod, "INSERT INTO MBAutojoin(Name) VALUES ('%s');" % channel)

def rehash():
    pass

def capskicker(cod, client, channel, line):
    pass



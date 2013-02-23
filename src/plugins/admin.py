# Copyright (c) 2013 Molly White
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN c.con WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re

def _is_admin(c, channel, line):
    '''Verify that the sender of a command is a bot admin.'''
    sender = c.get_sender(line)
    if sender in c.con._admins:
        return True
    else:
        c.con.say("Ask a bot admin to perform this for you.", channel)
        return False

def addadmin(c, channel, command_type, line):
    '''Adds an administrator to the list of bot admins.'''
    if (_is_admin(c, channel, line)):
        regex = re.compile("!?addadmin\s(.*)",re.IGNORECASE)
        r = re.search(regex, line)
        if r:
            message = r.group(1).split()
            if len(message) == 1:
                user = message[0]
                if user in c.con._admins:
                    c.con.say("{} is already a bot admin.".format(user), channel)
                else:
                    c.con._admins.append(user)
                    c.con.say("{} is now a bot admin.".format(user), channel)
            else:
                userlist = []
                for user in message:
                    if user in c.con._admins:
                        c.con._admins.append(user)
                        userlist.append(user)
                    else:
                        c.con.say("{} is already a bot admin.".format(user), channel)
                userlist = ', '.join(userlist)
                c.con.say("{} are now bot admins.".format(userlist), channel)
        else:
            c.con.say("Please specify which user to add.", channel)
            
            
def adminlist(c, channel, command_type, line):
    '''Prints a list of bot administrators.'''
    if len(c.con._admins) == 1:
        c.con.say("My bot admin is {}.".format(c.con._admins[0]), channel)
    else:
        adminlist = ', '.join(c.con._admins)
        c.con.say("My bot admins are: {}.".format(adminlist), channel)

def join(c, channel, command_type, line):
    '''Join a list of channels.'''
    if _is_admin(c, channel, line):
        regex = re.compile("!?join\s(.*)",re.IGNORECASE)
        r = re.search(regex, line)
        if r:
            chans = r.group(1).split()
            for chan in chans:
                c.con.join(chan)
        else:
            c.con.say("Please specify a channel to join (as !join #channel).", channel)
      
def emergencyshutoff(c, channel, command_type, line):
    '''Allows any user to kill the bot in case it malfunctions in some way.'''
    if command_type == "private":
        sender = c.get_sender(line)
        c.logger.error("Emergency shutdown requested by {}.".format(sender))
        c.con.say("Shutting down.", channel)
        c.con.shut_down()
    else:
        c.con.say("Please send this as a private message to shut me down.", channel)

def part(c, channel, command_type, line):
    '''Part a list of channels.'''
    if _is_admin(c, channel, line):
        regex = re.compile("!?part\s(.*)",re.IGNORECASE)
        r = re.search(regex, line)
        if r:
            chans = r.group(1).split()
            for chan in chans:
                c.con.part(chan)
        else:
            c.con.say("Please specify which channel to part (as !part #channel).", channel)
        
def ping(c, channel, command_type, line):
    '''Simple way to check if the bot is still functioning.'''
    c.con.say("Pong!", channel)
        
def quit(c, channel, command_type, line):
    '''Quits IRC, shuts down the bot.'''
    if _is_admin(c, channel, line):
        c.con.shut_down()

def shutdown(c, channel, command_type, line):
    '''Alias for quit'''
    quit(c, channel, command_type, line)

def removeadmin(c, channel, command_type, line):
    '''Removes an admin from the list of bot admins.'''
    if _is_admin(c, channel, line):
        regex = re.compile("!?removeadmin\s(.*)",re.IGNORECASE)
        r = re.search(regex, line)
        if r:
            users = r.group(1).split()
            for user in users:
                if user in c.con._admins:
                    if len(c.con._admins) == 1:
                        c.con.say("You are the only bot administrator. Please add another"
                                  " admin or disconnect the bot before removing yourself.", channel)
                        return 0
                    c.con._admins.remove(user)
                else:
                    c.con.say("{} is not on the list of bot admins.".format(user), channel)
                    users.remove(user)
            if len(users) == 1:
                c.con.say("{} is no longer a bot admin.".format(users[0]), channel)
            else:
                users = ', '.join(users)
                c.con.say("{} are no longer bot admins.".format(users), channel)
        else:
            c.con.say("Please specify which admin to remove.", channel)

# irc log parser
# read each line in a log file and sort it into one large file based on the timestamp of each line
# i created this because a volume had a stroke and i had to recover using photorec
# the recovery process was messy to say the least and it resulted in hundreds of files with various incorrect file names
# and a mix of logs and binary data.  i had dmesg output mixed with buffer logs, mixed with partial .deb packages, in files together with .gz extensions.
# maybe this will be helpful to someone some day.

# throw some logs into logpath, set the regex, set the various delimiters, and go nuts

# grab lines that are like YYYY-MM-DD HH:MM:SS  NICK    MESSAGE

# (r^(20)\d\d           --- line starts with year
# [-]                   --- separator
# (0[1-9]|1[012])       --- month
# [-]                   --- separator
# (0[1-9]|[12][0-9]|3[01])) --- day
# \d\d[:]\d\d[:]\d\d    --- time
# 	.*	.*      --- followed by two tabs and whatever

import os
import datetime
import re

logpath = os.getenv('HOME')+'/logs/'
dateregex = re.compile(r"^(20)\d\d[-](0[1-9]|1[012])[-](0[1-9]|[12][0-9]|3[01]) \d\d[:]\d\d[:]\d\d	.*	.*")
messagelist = []

# this is needed to define the sort item in the list.  i need to figure out how someone even figures this out from documentation
def getKey(item):
        return item[0]

for f in (os.listdir(logpath)):
	filename = open(logpath + f, 'r')
	nomatch = open('nomatch.txt', 'a')
	print(filename.name)
	for line in filename:
            # check if line matches regex, bingo bango, else that line into a second file for later analysis
            if dateregex.match(line):
                # chop up the entire line as lineparse, then put the date and time fields into datetimeparse
                lineparse = line.split('	',3)
                datetimeparse = lineparse[0]
                # chop out the date and the time from datetimeparse and put them into date and time respectively
                datetime = datetimeparse.split(' ',2)
                date = datetime[0]
                time = datetime[1]
                # chop out the year, month, and day from date and put it into ymdparse
                ymdparse = date.split('-',3)
                #  date = datetime[0], time = datetime[1], year = ymdparse[0], month = ymdparse[1], day = ymdparse[2], nick = lineparse[1], message = lineparse[2]
                messagelist.append([datetime[0], datetime[1], ymdparse[0], ymdparse[1], ymdparse[2], lineparse[1], lineparse[2]])
            else:
                # if date does not match regex output to a second file for analysis later
                nomatch.writelines(line)

# sort it!  store it!
messagelistsorted = sorted(messagelist, key = getKey)

# output it!
i = 0
while i < len(messagelistsorted):
        print(messagelistsorted[i])
        i += 1
        

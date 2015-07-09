#!/usr/bin/env python

###############
# Brian Burns
# bingpic.py
# Sets Bing image of the day as wallpaper
###############

#Imports
import os
import sys
import subprocess
import shutil
import urllib
from urllib2 import urlopen
from time import strftime
from xml.dom.minidom import parseString

# Official Bing Image of the Day RSS feed
feed = 'http://www.bing.com/HPImageArchive.aspx?format=rss&idx=0&n=1&mkt=en-US'

# Mac directory to store the image
directory = os.path.expanduser('~/Pictures/BingImage/')

APPLESCRIPT = """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
END"""

# Empties ~/$pictures/BingImage/
def emptyDir():
    # If ~/$pictures/BingImage/ doesn't exist simply return
    if not os.path.exists(directory):
        return
    # Delete each item in the directory
    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        try:
            # File
            if os.path.isfile(path):
                os.unlink(path)
            # Directory
            elif os.path.isdir(path):
                shutil.rmtree(path)
        except:
            print "Unable to empty ~/Pictures/BingImage"
            return

# Read Bing's RSS image feed and get the image of the day from it
def parseFeed(feedToParse):
    # Save the image as ~/$pictures/BingImage/MM-DD-YY.jpg
    imagePath = "%s%s.jpg" % (directory, strftime( "%m-%d-%y"))

    # Quit if today's image already exists
    if os.path.exists(imagePath):
        sys.exit(0)

    # If ~/$pictures/BingImage/ doesn't exist, create it
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Open the RSS feed
    try:
        rss = urlopen(feedToParse)
    except:
        print "Failed to open: %s" % feedToParse
        sys.exit(0)

    # Get the rss as a string
    rssString = rss.read()
    rss.close()
    # Create a dom object
    dom = parseString(rssString)
    # Get the bing image link
    link = dom.getElementsByTagName('link')[1]
    link = 'http://bing.com' + link.firstChild.nodeValue
    # Retreive the image
    urllib.urlretrieve(link, imagePath)

    # Return the image location
    return imagePath

# Change desktop picture on OS X
def changeMacBackground(imagePath):
    # Have osascript execute the AppleScript
    subprocess.Popen(APPLESCRIPT%imagePath, shell=True)

def main():
    # Empty ~/$pictures/BingImage/
    emptyDir()
    # Save the image and get its absolute path
    imagePath = parseFeed(feed)
    # Change the desktop background
    changeMacBackground(imagePath)

if __name__ == "__main__":
    main()

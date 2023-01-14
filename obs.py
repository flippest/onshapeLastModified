#!/usr/bin/env python3

import os
import platform
import time
import webbrowser

while True:
    os.system('./lastModified.py')
    with open("output.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            if "Link: " in line:
                # strip() to remove the trailing newline character
                link = line.split("Link: ")[1].strip()
                # Validate macOS before running the osascript command
                if platform.system() == "Darwin":
                    # Close all tabs in Chrome except the active tab
                    os.system('osascript -e "tell window 1 of application \\"Google Chrome\\" to close (tabs 1 thru (active tab index - 1))"')
                    #os.system("osascript -e 'tell application \"Google Chrome\" to close every tab of first window except for active tab'")
                webbrowser.open(link, new=0)
    time.sleep(60) # 1 minute

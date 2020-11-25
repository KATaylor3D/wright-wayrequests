# Quick rundown
### DBInterface.py
* First ui for this project _Stopped developing for the automatic email updates_
### Email.py
* Script for handling the email
### general.py
* A couple random alarm test scripts used to indicate a problem scraping
* The Scraper is throttled to slow down the get requests as to not get banned from the site for being a bot
### main.py
* The recursive script that contains all the logic
## _This is the script to be run with python3 main.py_
### Scraper.py
* The script used to scrape the site
### Sqlick.py
* Script that has simplified SQLite3 functions and methods
### concant.txt
* Place to hold any scrape that is incomplete and unable to be put into the SQL table
### last.txt
* Holds the length of the last scrape to be used to deteremine if a full scrape is needed
### message.txt
* Template used to create the content used in the email

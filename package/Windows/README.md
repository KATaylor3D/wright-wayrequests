# How to run
* In command prompt change directory to where these files are located on your computer
* Run it by typing python3 main.py
* Enter in email, smtp.email, and the app password that was generated earlier
* The initial run will build your database and send all available dogs from the shelter to your email.
* _This email will be long_
* Just leave the script running and anytime the website uploads new dogs they will be sent to you in 3 minutes or less
## _This is the script to be run with python3 main.py_
# Quick rundown of files
### DBInterface.py
* First ui for this project _Stopped developing for the automatic email updates_
### Email.py
* Script for handling the email
### general.py
* A couple random alarm test scripts used to indicate a problem scraping
* The Scraper is throttled to slow down the get requests as to not get banned from the site for being a bot
### main.py
* The recursive script that contains all the logic
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

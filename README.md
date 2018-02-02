# FeelsGoodMan-TwitterBot
Prints "FeelsGoodMan" onto landscape images from Reddit and tweets these images to Twitter @FeelsGoodManBot hourly.

This python script uses PRAW, PIL, and Twython.

PRAW (The Python Reddit API Wrapper):
  - searches through X number of posts (currently 100) and puts them into a list named postList
PIL (Python Imaging Library):
  - writes text onto images (currently "FeelsGoodMan") and saves image
Twython:
  - a twitter/python interface that allows for Twitter actions to be executed in python scripts


Script Process:
  - if the list of posts is empty, request the newest 100 posts from Reddit.com/r/EarthPorn
  - pick a random post from the list and check if it is useable
  - posts are usable if they are linked from imgur.com
  - if from imgur.com and do not have ".gif, .jpg, .jpeg, .png" at the end of the URL, append .jpg
  - if the post is not linked from imgur, delete the list element and try a new random post (repeat as needed)
  - once an image is found and is useable, save to device under the current directory in a folder named "SavedImages" under the file name "image"
  - check to see if image is over the max file size and resolution able to be tweeted
  - open image and auto size the font (which is Lato-Regular.ttf) to be 70% the width
  - print message (currently FeelsGoodMan) onto image, centered vertically and horizontally
  - save image with message printed on it to "SavedImages" under the file name "imageText"
  - reopen the image (needed to keep Twython happy)
  - attempt to Tweet image with message on it, if failed sleep for 15 minutes and try from the top again
  - repeat forever, ~hourly

How to get the script working on your machine:
*NOTE: this is running off a Raspberry Pi 2 running Raspian*
*some other configurations may be needed on other machines*

- install PIL     ~ pip3 install PIL
- install PRAW    ~ pip3 install PRAW
- install twython ~ pip3 install twython
- create a auth.py and put in the same directory as this file
- create a Twitter account (this will be the account that tweets the images)
- create a new Twitter app (apps.twitter.com)
- create new tokens and refresh page
- save your consumer key, consumer secret, access token, access token secret as
            consumer_key, consumer_secret, access_token, and access_token_secret respectively in auth.py
- create a Reddit account
- go to https://www.reddit.com/prefs/apps and follow the steps to create new app at the bottom
- acquire your app ID and ID secret
- save your username, password, ID, and ID secret as
            usr, pswd, ID, and IDsecret respectively in auth .py
- finished!

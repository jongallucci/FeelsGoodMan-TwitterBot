import os, io, praw, random, requests, time
from PIL import Image, ImageDraw, ImageFont

from twython import Twython
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
    usr,
    pswd,
    ID,
    IDsecret
)

twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

def sleepTime(seconds, n):
    print("Sleeping For", seconds,"Seconds")
    for i in range(0, n):
        time.sleep(seconds//n)
        print(seconds//n*(i+1),"Seconds Have Elapsed")
    print("Starting Again")
#------------------------#

r = praw.Reddit(client_id = ID,
                client_secret = IDsecret,
                user_agent = "Tweet Earthporn images with message on top.",
                password = pswd,
                username = usr)

getCount = 100
timeInterval = 3600 #seconds
subredditName = "EarthPorn"
EXTENSIONS = ['.gif', '.jpg', '.jpeg', '.png']

postList = []
while True:

    if len(postList) == 0:
        print("Getting ", getCount," Images From r/", subredditName, sep = "")
        sub = r.subreddit(subredditName)
        postList = sub.new(limit = getCount)

        tempList = []
        for post in postList:      #turn postList into a PythonList
            tempList.append(post)
        postList = tempList

    randPost = random.randint(0, len(postList) - 1)

    submission = postList[randPost]
    if 'imgur.com/' not in submission.url:
        del postList[randPost]
        continue
    if not any(extension in submission.url for extension in EXTENSIONS):
        submission.url += '.jpg'

    postURL = postList[randPost].url
    del postList[randPost]
    print("Number Of Posts Left In List:",len(postList))

    print(postURL)
    img = requests.get(postURL)

    open('SavedImages/image', 'wb').write(img.content)
    print("Saved")

    imgToTweet = Image.open('SavedImages/image')
    print("Opened")
    fileSize = os.stat('SavedImages/image')
    if fileSize.st_size > 5242880 or imgToTweet.width > 8192 or imgToTweet.height > 8192:
        print("Image Too Large, Retrying..")
        continue
    draw = ImageDraw.Draw(imgToTweet)

    message = "FeelsGoodMan"
    fontsize = 1
    img_fraction = 0.70
    font = ImageFont.truetype(".font/Lato-Regular.ttf", fontsize)
    while font.getsize(message)[0] < img_fraction*imgToTweet.size[0]:
        fontsize += 1
        font = ImageFont.truetype(".font/Lato-Regular.ttf", fontsize)
    fontsize -= 1
    font = ImageFont.truetype(".font/Lato-Regular.ttf", fontsize)

    draw.text((imgToTweet.width/2 - font.getsize(message)[0]/2,imgToTweet.height/2 - font.getsize(message)[1]/2), message, (255,255,255), font = font)
    draw = ImageDraw.Draw(imgToTweet)
    print("Drawn On")
    imgToTweet.save("SavedImages/imageText", "JPEG")
    print("Saved With Text")
    imgToTweet = open("SavedImages/imageText", "rb")
    try:
        tweet = twitter.upload_media(media = imgToTweet)
        twitter.update_status(status = "#FeelsGoodMan", media_ids = [tweet["media_id"]])
    except:
        print("Post Failed, Retry From The Top")
        time.sleep(900)  # 15 minutes
        continue

    print("Tweeted: '%s'" % message)
    sleepTime(timeInterval, 4)

#twitter.update_status(status = message)

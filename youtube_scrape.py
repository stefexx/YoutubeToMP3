from pytube import YouTube, Playlist
SAVE_PATH = "C:/Users/Stefan/youtubescrape/songs"
playlist_url = "https://youtube.com/playlist?list=PLedrohii4LSDxUp0hGulVO41ez-UylY07"

try:
    p = Playlist(playlist_url)
except:
    print("Playlist cannot be found")

for url in p.video_urls:
    try:
        yt = YouTube(url)
    except:
        print(f"{url.title} is unavailable, skipping")
    else:
        print(f"Downloading video: {yt.title}")
        stream = yt.streams.get_by_itag(140)
        stream.download(SAVE_PATH)

        
#i finally understand the problem with downlaoding podcats. They are too large and email only allows 25MB to be sent at once.
#  Also there are no file extension for mp3?.
# For example a 1.3 hr podcat is approx 75MB, so approx 25 min = 25MB, so somehow limit the file size to 25mb, and send seperate emails,
# or figure out something completely different, probaly create a new function that detects if the filesize is >25MB then,
#donwlaod the video in a spereated folder
#options
#1. split the videos into 25Mb bits (kinda lame)
#2. downlaod the videos manually with usb cable (even more lame)
#3. download video by compressing, or send a google drive link? (maybe, option 2 is not bad)


#To send email with downloaded songs to you
import smtplib
import os
from email.message import EmailMessage
file_list = os.listdir(SAVE_PATH)
print(file_list)

email_address = os.environ.get('email_address')
email_password = os.environ.get('email_password')

msg = EmailMessage()
msg['Subject'] = "Your Weekly Dose of Music."
msg['From'] = email_address
msg['To'] = email_address
msg.set_content('Muisc attached...')

#change html to look awesome
with open('email_template.html', 'r') as f:
    html_file = f.read()
msg.add_alternative(html_file, subtype='html')

try:
    for file in file_list:
        file_path = os.path.join(SAVE_PATH, file)
        with open(file_path, 'rb') as f:
            file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file)
        os.remove(file_path)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)

        smtp.send_message(msg)
        print("Email sent succesfully!")

except:
    print("Error when sending email!")

#script to delete items from playlist
import delete_playlist_item 
delete_playlist_item.main()

# TODO:
#udpate html to make a cool email template optional as its kinda trivial
#add comments to everythings so you rememebr how to do this
#eventualy learn how to push onto git, how to publish code
# and how top write documenttion
#this will be a later problem from you and you will
#probaly forget everythiong but thats ok
#add a try except function for the delte playlist part

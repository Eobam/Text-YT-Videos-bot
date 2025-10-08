#Imports
import yt_dlp 
from moviepy import VideoFileClip
import subprocess
import os

#Gets the video, I think...
def download_youtube_video(url):
    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'bestvideo+bestaudio/best'
        'noplaylist': True
        #line 11, probs gonna be removed, seems useless, tutorial says otherwise tho
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        
    return 'video.mp4'


#Converts to textable format (TBD whether it'll be .mov or .mp4)
def convert_to_mov(input_file):
    clip = VideoFileClip(input_file)
    clip.write_videofile("video.mov", codec="libx264")
    return "video.mov"

#Sends the text
def send_imessage(phone_number, file_path):
    script = f'''
    tell application "Messages"
        set targetService to 1st service whose service type = iMessage
        set targetBuddy to buddy "{phone_number}" of targetService
        send POSIX file "{os.path.abspath(file_path)}" to targetBuddy
    end tell
    '''
    subprocess.run(["osascript", "-e", script])
    #copied the above code block from StackOverflow ts is gonna break...

if __name__ == "__main__":
    url = input("Video Link Please: ")
    video_file = download_youtube_video(url)
    mov_file = convert_to_mov(video_file)

    print("If dis worked, you'll see this oh and btw this should be the name of the video file", mov_file)
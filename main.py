#Imports
import yt_dlp 
from moviepy import VideoFileClip
import subprocess
import os
from yt_dlp import YoutubeDL
from datetime import datetime
import tempfile
import random
import time


#Gets the video, I think...
def download_youtube_video(url):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.abspath(f"video_{timestamp}.mp4")
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'retries': 10,
        'socket_timeout': 30,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    delay = random.uniform(15, 60)
    print(f"{int(delay)} until next request")
    time.sleep(delay)
    return output_path
#attempt at not getting rate limited ^


#Converts to textable format (TBD whether it'll be .mov or .mp4)
def convert_to_mov(input_file):
    clip = VideoFileClip(input_file)
    mov_path = input_file.replace(".mp4", ".mov")
    clip.write_videofile(mov_path, codec='libx264', audio_codec='aac')
    clip.close()
    return mov_path
    #ermmmm, I think this breaks it, note to self: If code doesn't work, debug this

#Sends the text
def send_imessage(phone_number, video_path):
    script = f'''
    tell application "Messages"
        set targetService to 1st service whose service type = iMessage
        set targetBuddy to buddy "{phone_number}" of targetService
        send POSIX file "{video_path}" to targetBuddy
    end tell
    '''
    with tempfile.NamedTemporaryFile(mode="w", suffix=".applescript", delete=False) as f:
        f.write(script)
        temp_path = f.name

    try:
        subprocess.run(["osascript", temp_path], check=True)
    finally:
        os.remove(temp_path)

#uhhh, this is supposed to fix the zsh error according to a random man with an insane accent so obvi gonna work.


if __name__ == "__main__":
    url = input("Video Link Please: ")
    phone_number = input("gimme yo digits")
    if phone_number == " ": 
        print("broski, gimme your frickin digits")
        phone_number = input("come on now, hand em over")
    mp4_path = download_youtube_video(url)
    mov_file = convert_to_mov(mp4_path)
    video_file = convert_to_mov(mp4_path)
    send_imessage(phone_number, mov_file)


    print("If dis worked, you'll see this oh and btw this should be the name of the video file", mov_file)


def get_video_info(url):
    ydl_opts = {"quiet": True, "skip_download": True}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            "title": info.get("title"),
            "uploader": info.get("uploader"),
            "uploader_url": info.get("uploader_url"),
            "description": info.get("description"),
            "duration": info.get("duration"),

        }
def print_info():
    ydl_opts = {"quiet": True, "skip_download": True}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            "title": info.get("title"),
            "uploader": info.get("uploader"),
            "uploader_url": info.get("uploader_url"),
            "description": info.get("description"),
            "duration": info.get("duration"),
        }
    

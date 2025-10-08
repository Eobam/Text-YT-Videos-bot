#Imports
import yt_dlp 
from moviepy import VideoFileClip
import subprocess
import os
from yt_dlp import YoutubeDL

#Gets the video, I think...
def download_youtube_video(url):
    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'noplaylist': True
        #line 11, probs gonna be removed, seems useless, tutorial says otherwise tho
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)
    merged_file = filename.rsplit('.', 1)[0] + '.webm'
    if os.path.exists(merged_file):
        return merged_file
    return filename


#Converts to textable format (TBD whether it'll be .mov or .mp4)
def convert_to_mov(input_file):
    clip = VideoFileClip(input_file)
    clip.write_videofile("video.mov", codec="libx264")
    return "video.mov"

#Sends the text
def send_imessage(phone_number, file_path, attachment_path=None):
    script = f'''
    tell application "Messages"
        set targetService to 1st service whose service type = iMessage
        set targetBuddy to buddy "{phone_number}" of targetService
        send "{message}" to targetBuddy
    end tell
    '''
    subprocess.run(["osascript", "-e", script])
    #copied the above code block from StackOverflow ts is gonna break...

    if attachment_path:
        applescript += f'\n        send POSIX file "{attachment_path}" to targetBuddy'
    applescript += '\nend tell'

    subprocess.run(["osascript", "-e", applescript])

if __name__ == "__main__":
    url = input("Video Link Please: ")
    video_file = download_youtube_video(url)
    mov_file = convert_to_mov(video_file)

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
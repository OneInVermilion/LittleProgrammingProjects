from pytube import YouTube
import os

"""
GUI
    video highest res
    video lowerst res
    audio
    thumbnail
"""

def download_video(url, mode, new_name=""):
    vid = YouTube(url)
    match mode:
        case 1: #high res
            vid_dwnl = vid.streams.get_highest_resolution()
        case 2: #low res
            vid_dwnl = vid.streams.get_lowest_resolution()
        case 3: #audio
            vid_dwnl = vid.streams.get_audio_only()
        case _:
            print("ERROR")
    downloaded_file = vid_dwnl.download()
    base_name, extension = os.path.splitext(downloaded_file)
    if mode == 3:
        extension = ".mp3"
    if new_name != "":
        base_name = new_name
    os.rename(downloaded_file, base_name + extension)

url = input("URL:\n")
mode = int(input("1 - Highest Resolution\n2 - Lowest Resolution\n3 - Audio Only\n"))
name = input("File Name (Leave Blank for YouTube's Video Name):\n")
print("\nDownloading...")
download_video(url, mode, name)
input("Downloading Finished. Press Enter to Exit")

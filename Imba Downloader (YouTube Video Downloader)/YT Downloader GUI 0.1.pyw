from pytube import YouTube
import os
from tkinter import *
from tkinter import ttk
import threading
from datetime import datetime

#https://thepythoncode.com/article/make-a-youtube-video-downloader-in-python

def datentime():
    now = datetime.now()
    return(now.strftime(" %d.%m.%Y %H-%M-%S"))

def download_video(url, mode, new_name=""):
    try:
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
        #base_name += datentime()
        os.rename(downloaded_file, base_name + extension)
    except:
        print("error")

def dv_hr():
    url = url_entry.get()
    new_name = name_entry.get()
    download_video(url, 1, new_name)

def dv_lr():
    url = url_entry.get()
    new_name = name_entry.get()
    download_video(url, 2, new_name)

def dv_au():
    url = url_entry.get()
    new_name = name_entry.get()
    download_video(url, 3, new_name)

def thread_hr():
    t = threading.Thread(target=dv_hr)
    t.start()

def thread_lr():
    t = threading.Thread(target=dv_lr)
    t.start()

def thread_au():
    t = threading.Thread(target=dv_au)
    t.start()
"""
url = input("URL:\n")
mode = int(input("1 - Highest Resolution\n2 - Lowest Resolution\n3 - Audio Only\n"))
name = input("File Name (Leave Blank for YouTube's Video Name):\n")
print("\nDownloading...")
download_video(url, mode, name)
input("Downloading Finished. Press Enter to Exit")
"""
w = 800
h = 400
window = Tk()
window.title("Imba downloader")
window.geometry(str(w) + "x" + str(h))
window.resizable(False, False)

canvas = Canvas(window, {"bg": "black", "width": w, "height": h})
canvas.pack()

text1_label = Label(window, text="Enter URL:")
canvas.create_window(w*0.5, 50, window=text1_label)

url_entry = Entry(window, width=int(w/8))
canvas.create_window(w*0.5, 75, window=url_entry)

text2_label = Label(window, text="File Name (Leave Blank for Youtube's Video Name):")
canvas.create_window(w*0.5, 125, window=text2_label)

name_entry = Entry(window, width=int(w/8))
canvas.create_window(w*0.5, 150, window=name_entry)

dwnl_highres_btn = Button(window, text="Download\nHighest Resolution", width=16, height=4, command=thread_hr)
canvas.create_window(w*0.25, 250, window=dwnl_highres_btn)

dwnl_lowres_btn = Button(window, text="Download\nLowest Resolution", width=16, height=4, command=thread_lr)
canvas.create_window(w*0.5, 250, window=dwnl_lowres_btn)

dwnl_audio_btn = Button(window, text="Download\nAudio Only", width=16, height=4, command=thread_au)
canvas.create_window(w*0.75, 250, window=dwnl_audio_btn)

pb = ttk.Progressbar(window, orient=HORIZONTAL, length=w*0.75, mode="indeterminate")
canvas.create_window(w*0.5, 350, window=pb)

window.mainloop()

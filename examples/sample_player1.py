# Author Paul

# MIT License
#
# Copyright (c) 2021 Paul
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# This is same as sample_player example but this doesn't makes use of control variable to update the slider

# import sys
# sys.path.append('./')

import datetime
import tkinter as tk
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo
import cv2
import math

import draw_bbx_main

input_file_path = ""

def update_duration(event):
    """ updates the duration after finding the duration """
    duration = vid_player.video_info()["duration"]
    end_time["text"] = str(datetime.timedelta(seconds=duration))
    progress_slider["to"] = duration


def update_scale(event):
    """ updates the scale value """
    progress_slider.set(vid_player.current_duration())


def load_video():
    """ loads the video """
    file_path = filedialog.askopenfilename()

    if file_path:
        vid_player.load(file_path)
        global input_file_path 
        input_file_path = file_path
        #print(input_file_path)
        progress_slider.config(to=0, from_=0)
        play_pause_btn["text"] = "Play"
        progress_slider.set(0)


def seek(event=None):
    """ used to seek a specific timeframe """
    vid_player.seek(int(progress_slider.get()))


def skip(value: int):
    """ skip seconds """
    vid_player.seek(int(progress_slider.get())+value)
    progress_slider.set(progress_slider.get() + value)


def play_pause():
    """ pauses and plays """
    if vid_player.is_paused():
        vid_player.play()
        play_pause_btn["text"] = "Pause"

    else:
        vid_player.pause()
        #print(vid_player.current_duration())
        play_pause_btn["text"] = "Play"


def video_ended(event):
    """ handle video ended """
    progress_slider.set(progress_slider["to"])
    play_pause_btn["text"] = "Play"
    progress_slider.set(0)

def capture_frame_from_vid():
    #print(vid_player.current_duration()) 
    global input_file_path
    print(input_file_path)
    vidcap = cv2.VideoCapture(input_file_path)
    
    #https://queirozf.com/entries/python-number-formatting-examples
    #truncating he value then padding with zeros to the right
    print('{:<04}'.format(math.trunc(vid_player.current_duration())))
    vidcap.set(cv2.CAP_PROP_POS_MSEC,float('{:<04}'.format(math.trunc(vid_player.current_duration()))))      # just cue to nth sec. position
    success,image = vidcap.read()
    if success:
        cv2.imwrite("../captured_frames_folder/frame20sec.jpg", image)     # save frame as JPEG file
        cv2.imshow("20sec",image)
        #cv2.waitKey()     


root = tk.Tk()
root.title("Tkinter media")

load_btn = tk.Button(root, text="Load", command=load_video)
load_btn.pack()

capture_frame = tk.Button(root, text="Capture Frame", command=capture_frame_from_vid)
capture_frame.pack()

get_region_of_interest = tk.Button(root, text="get region of interest", command = lambda:draw_bbx_main.draw_bbx_MAIN("../captured_frames_folder/frame20sec.jpg"))
get_region_of_interest.pack()

vid_player = TkinterVideo(scaled=True, master=root)
vid_player.pack(expand=True, fill="both")

play_pause_btn = tk.Button(root, text="Play", command=play_pause)
play_pause_btn.pack()

skip_plus_5sec = tk.Button(root, text="Skip -5 sec", command=lambda: skip(-5))
skip_plus_5sec.pack(side="left")

start_time = tk.Label(root, text=str(datetime.timedelta(seconds=0)))
start_time.pack(side="left")

progress_slider = tk.Scale(root, from_=0, to=0, orient="horizontal")
progress_slider.bind("<ButtonRelease-1>", seek)
progress_slider.pack(side="left", fill="x", expand=True)

end_time = tk.Label(root, text=str(datetime.timedelta(seconds=0)))
end_time.pack(side="left")

vid_player.bind("<<Duration>>", update_duration)
vid_player.bind("<<SecondChanged>>", update_scale)
vid_player.bind("<<Ended>>", video_ended )

skip_plus_5sec = tk.Button(root, text="Skip +5 sec", command=lambda: skip(5))
skip_plus_5sec.pack(side="left")

root.mainloop()

#Souce: https://www.plus2net.com/python/tkinter-filedialog-upload-display.php

#import draw_bounding_box_test_1.draw_bbx_main

import os

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
import cv2
import numpy as np

import  draw_bbx_main



my_w = tk.Tk()
my_w.geometry("600x600")  # Size of the window 
my_w.title('www.plus2net.com')
my_font1=('times', 18, 'bold')
l1 = tk.Label(my_w,text='TRMC Auto Augmenter',width=30,font=my_font1)  
l1.grid(row=1,column=1)
b1 = tk.Button(my_w, text='Upload File', 
   width=20,command = lambda:upload_file())
b1.grid(row=1,column=2) 





def upload_file():
    #getting image from local directory
    global img
    f_types = [('Jpg Files', '*.jpg')]
    filename_with_path = filedialog.askopenfilename(filetypes=f_types)
    display_img = ImageTk.PhotoImage(file=filename_with_path)

    #using cv2 to read in then write out image to  "input_pic_hold"
    img_file = cv2.imread(filename_with_path, 1)
    directory = "input_pic_hold"
    os.chdir(directory)
    cv2.imwrite("new_cropped_img.jpeg", img_file)
    print(img_file)

    b2 =tk.Button(my_w,image=display_img) # using Button 
    b2.grid(row=3,column=1)
    b3 = tk.Button(my_w, text='Get Region of Interest', 
    width=20,command = lambda:draw_bbx_main.draw_bbx_MAIN(filename_with_path))
    b3.grid(row=2,column=2) 



my_w.mainloop()  # Keep the window open

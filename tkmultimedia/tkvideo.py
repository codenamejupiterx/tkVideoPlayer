import av
import time
import threading
import tkinter as tk
from PIL import ImageTk, Image
from typing import Tuple


# todo: try directly playing the file like container.decode(video=0)[self._frame_number].to_image
class TkinterVideo(tk.Label):

    def __init__(self, scaled: bool = False, pre_load: bool = False, *args, **kwargs):
        super(TkinterVideo, self).__init__(*args, **kwargs)

        self.image_sequence = []
        self.current_imgtk = None
        self.current_img = None
        self.load_thread = None

        self._frame_rate = 1
        self._frame_size = (100, 75)
        self._frame_number = 0

        self._current_size = (50, 50)

        self.preload = pre_load
        self._loaded = False
        self._paused = True
        self._playing = False

        self.set_scaled(scaled)

    def set_scaled(self, scaled=bool):
        self.scaled = scaled

        if scaled:
            self.bind("<Configure>", self.resize_event)

        else:
            self.unbind("<Configure>")

    def resize_event(self, event):

        self._current_size = event.width, event.height

        if self._paused and self.current_img:
            self.current_img = self.image_sequence[self._frame_number].copy().resize(self._current_size)
            self.current_imgtk = ImageTk.PhotoImage(self.current_img)
            self.config(image=self.current_img)

    def _set_frame_size(self, event=None):

        self.current_imgtk = ImageTk.PhotoImage(Image.new("RGBA", self._frame_size, (255, 0, 0, 0)))
        self.config(width=self._frame_size[0], height=self._frame_size[1], image=self.current_imgtk)

    def _load(self, file_path: str):
        """ loads the frames from a thread """

        try:
            with av.open(file_path) as container:
                self._frame_rate = int(container.streams.video[0].average_rate)
                self._frame_size = (container.streams.video[0].width, container.streams.video[0].height)
                self._set_frame_size()

                if self.preload:
                    self.image_sequence = [frame.to_image() for frame in container.decode(video=0)]

                else:
                    for frame in container.decode(video=0):
                        self.image_sequence.append(frame.to_image())

            self._loaded = True
            self.event_generate("<<loaded>>")

        except Exception as e:
            raise e

    def load(self, file_path=""):
        """ loads the video and generates <<loaded>> event after loading """
        self.image_sequence = []

        self.load_thread = threading.Thread(target=self._load, args=(file_path,), daemon=True)
        self.load_thread.start()

    def loaded(self) -> bool:
        """ returns whether the video has been loaded """
        return self._loaded

    def frame_size(self) -> Tuple[int, int]:
        """ return frame dimension """
        return self._frame_size

    def frame_rate(self) -> float:
        """ returns the current frame rate """
        return self._frame_rate

    def frame(self) -> Tuple[tk.Image, int, float]:
        """ return current frame image, frame number and frame rate  """
        return self.current_img, self._frame_number, self._frame_rate

    def play(self):
        """ plays the loaded video """
        self._playing = True

        if self._frame_number == len(self.image_sequence):
            self._frame_number = 0

        self.bind("<<FrameGenerated>>", self._display_frame)
        if not self.preload:
            self._paused = False
            self._playing_thread = threading.Thread(target=self._update_frames, daemon=True)
            self._playing_thread.start()

        else:
            self.bind("<<loaded>>", self._start_loaded)

    def _start_loaded(self, event):

        self._paused = False
        # self._display_frame()
        self._playing_thread = threading.Thread(target=self._update_frames, daemon=True)
        self._playing_thread.start()

    def is_paused(self) -> bool:
        """ returns if the video is paused """
        return self._paused

    def pause(self):
        """ pauses the video """
        self._paused = True

    def stop(self):
        """ stop removes the loaded video and reset the frame_number"""
        self.playing = False
        self._paused = True
        self._frame_number = 0
        self.image_sequence = []

    def skip_sec(self, sec: int):
        """ skip by seconds """
        pass

    def skip_frames(self, number_of_frames: int):
        """ skip by how many frames +ve or -ve """

        if number_of_frames < 0 and (self._frame_number - number_of_frames) > 0:
            self._frame_number -= number_of_frames

        elif number_of_frames > 0 and (self._frame_number + number_of_frames) > len(self.image_sequence):
            self._frame_number += number_of_frames

    def _update_frames(self):
        """ updates frame from thread """

        now = time.time_ns() // 1_000_000  # time in milliseconds
        then = now
        print("updating...")

        test_time = time.time()
        previous_time = test_time

        while self._playing:

            # if self._frame_number >= len(self.image_sequence):
            #     break

            if not self._paused and self._frame_number < len(self.image_sequence) - 1:

                now = time.time_ns() // 1_000_000
                delta = now - then  # time difference between current frame and previous frame
                then = now

                if delta == 0:
                    delta = 1

                # print(delta, 1/self._frame_rate, 1/(self._frame_rate * delta))

                self.current_img = self.image_sequence[self._frame_number].copy()

                if self.scaled:
                    self.current_img = self.current_img.resize(self._current_size)

                self.event_generate("<<FrameGenerated>>")

                self._frame_number += 1
                if self._frame_number % 30 == 0:
                    test_time = time.time()
                    print("Frame Reached: ", self._frame_number, self.frame_rate(), test_time - previous_time)
                    previous_time = test_time

                # print(delta / 1000, 1 / self._frame_rate)

                if delta / 1000 >= 1 / self._frame_rate:
                    continue

                # print("Continuing...: ", (1 / self._frame_rate) - (delta / 1000))
                # time.sleep((delta/1000)+((1/self._frame_rate) - (delta/1000)))
                time.sleep((1 / self._frame_rate) - (delta / 1000))
                continue

            if not self.preload:
                time.sleep(0.0015)

        self._playing = False
        self._paused = True

    def _display_frame(self, event):
        """ updates the image in the label """

        # if self._playing and not self._paused:
        # print("Updating....")

        self.current_imgtk = ImageTk.PhotoImage(self.current_img)
        self.config(image=self.current_imgtk)

# root = tk.Tk()
#
# tkvideo = TkinterVideo(master=root, scaled=False, pre_load=False)
# # tkvideo.load(r"C:\Users\Paul\Videos\VID-20180328-WA0050.mp4")
# tkvideo.load(r"sampledata\samplevideo.mp4")
# tkvideo.pack(expand=True, fill="both")
#
# tkvideo.play()
#
# root.mainloop()
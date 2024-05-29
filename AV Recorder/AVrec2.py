import itertools

import cv2
import pyaudio
import wave
import threading
import time
import subprocess
import os
import AudioManip

current_dir = "Testing"
current_file_name = "temp"
sent_display = ""


########################
## JRF
## VideoRecorder and AudioRecorder are two classes based on openCV and pyaudio, respectively.
## By using multithreading these two classes allow to record simultaneously video and audio.
## ffmpeg is used for muxing the two signals
## A timer loop is used to control the frame rate of the video recording. This timer as well as
## the final encoding rate can be adjusted according to camera capabilities
##

########################
## Usage:
##
## numpy, PyAudio and Wave need to be installed
## install openCV, make sure the file cv2.pyd is located in the same folder as the other libraries
## install ffmpeg and make sure the ffmpeg .exe is in the working directory
##
##
## start_AVrecording(filename) # function to start the recording
## stop_AVrecording(filename)  # "" ... to stop it
##
##
########################


class VideoRecorder():

    # Video class based on openCV
    def __init__(self):

        self.open = True
        self.device_index = 1
        self.fps = 25  # fps should be the minimum constant rate at which the camera can
        self.fourcc = "MJPG"  # capture images (with no decrease in speed over time; testing is required)
        self.frameSize = (640, 480)  # video formats and sizes also depend and vary according to the camera used
        self.video_filename = current_file_name + "_video.avi"
        self.video_cap = cv2.VideoCapture(self.device_index)
        self.video_writer = cv2.VideoWriter_fourcc(*self.fourcc)
        self.video_out = cv2.VideoWriter(self.video_filename, self.video_writer, self.fps, self.frameSize)
        self.frame_counts = 1
        self.start_time = time.time()

    # Video starts being recorded
    def record(self):

        #		counter = 1
        timer_start = time.time()
        timer_current = 0

        while (self.open == True):
            ret, video_frame = self.video_cap.read()
            if (ret == True):

                self.video_out.write(video_frame)
                #					print str(counter) + " " + str(self.frame_counts) + " frames written " + str(timer_current)
                self.frame_counts += 1
                #					counter += 1
                #					timer_current = time.time() - timer_start
                # time.sleep(0.04)

                # Uncomment the following three lines to make the video to be
                # displayed to screen while recording
                # font
                font = cv2.FONT_HERSHEY_SIMPLEX
                # org
                org = (50, 50)
                # fontScale
                fontScale = 1
                # Blue color in BGR
                color = (255, 0, 0)
                # Line thickness of 2 px
                thickness = 2
                # gray = cv2.cvtColor(video_frame, cv2.COLOR_RGB2BGR)

                image = cv2.putText(video_frame, sent_display, org, font, fontScale, color, thickness, cv2.LINE_AA)
                cv2.imshow('video_frame', image)
                cv2.waitKey(1)
            else:
                break

            # 0.16 delay -> 6 fps
            #

    # Finishes the video recording therefore the thread too
    def stop(self):

        if self.open == True:

            self.open = False
            self.video_out.release()
            self.video_cap.release()
            cv2.destroyAllWindows()

        else:
            pass

    # Launches the video recording function using a thread
    def start(self):
        video_thread = threading.Thread(target=self.record)
        video_thread.start()


class AudioRecorder():

    # Audio class based on pyAudio and Wave
    def __init__(self):

        self.open = True
        self.rate = 48000
        self.frames_per_buffer = 1024
        self.channels = 1
        self.format = pyaudio.paInt16
        self.audio_filename = current_file_name + "_audio.wav"
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.frames_per_buffer)
        self.audio_frames = []

    # Audio starts being recorded
    def record(self):

        self.stream.start_stream()
        while (self.open == True):
            data = self.stream.read(self.frames_per_buffer)
            self.audio_frames.append(data)
            if self.open == False:
                break

    # Finishes the audio recording therefore the thread too
    def stop(self):

        if self.open == True:
            self.open = False
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()

            waveFile = wave.open(self.audio_filename, 'wb')
            waveFile.setnchannels(self.channels)
            waveFile.setsampwidth(self.audio.get_sample_size(self.format))
            waveFile.setframerate(self.rate)
            waveFile.writeframes(b''.join(self.audio_frames))
            waveFile.close()

        pass

    # Launches the audio recording function using a thread
    def start(self):
        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()


def start_AVrecording():
    global video_thread
    global audio_thread

    video_thread = VideoRecorder()
    audio_thread = AudioRecorder()

    audio_thread.start()
    video_thread.start()


def start_video_recording():
    global video_thread

    video_thread = VideoRecorder()
    video_thread.start()


def start_audio_recording():
    global audio_thread

    audio_thread = AudioRecorder()
    audio_thread.start()


def stop_AVrecording():
    audio_thread.stop()
    frame_counts = video_thread.frame_counts
    elapsed_time = time.time() - video_thread.start_time
    recorded_fps = frame_counts / elapsed_time
    print("\ntotal frames " + str(frame_counts))
    print("elapsed time " + str(elapsed_time))
    print("recorded fps " + str(recorded_fps))
    video_thread.stop()

    # Makes sure the threads have finished
    while threading.active_count() > 1:
        time.sleep(1)

    #	 Merging audio and video signal

    if abs(recorded_fps - 25) >= 0.01:  # If the fps rate was higher/lower than expected, re-encode it to the expected
        m = 1
        #print
        #"Re-encoding"
        #cmd = "ffmpeg -r " + str(
            #recorded_fps) + " -i " + current_file_name + "_video.avi -pix_fmt yuv420p -r 25 " + current_file_name + "_video2.avi"
        #subprocess.call(cmd, shell=True)

        # print
        # "Muxing"
        # cmd = "ffmpeg -ac 2 -channel_layout mono -i " + current_file_name + "_audio.wav -i " + current_file_name + "_video2.avi  " + current_file_name + "_AV2.avi"
        # subprocess.call(cmd, shell=True)

        #cmd = "ffmpeg -i " + current_file_name + "_video.avi -i " + current_file_name + "_audio.wav -c copy " + current_file_name + "_AV.avi"
        #subprocess.call(cmd, shell=True)


    else:
        m=1
        # print
        # "Normal recording\nMuxing"
        # cmd = "ffmpeg -ac 2 -channel_layout mono -i " + current_file_name + "_audio.wav -i " + current_file_name + "_video.avi " + current_file_name + "_AV2.avi"
        # subprocess.call(cmd, shell=True)

        #cmd = "ffmpeg -i " + current_file_name + "_video.avi -i " + current_file_name + "_audio.wav -c copy " + current_file_name + "_AV.avi"
        subprocess.call(cmd, shell=True)

        print
        ".."


# Required and wanted processing of final files
def file_manager():
    local_path = os.getcwd()

    if os.path.exists(local_path + "/" + current_file_name + "_audio.wav"):
        os.remove(local_path + "/" + current_file_name + "_audio.wav")

    if os.path.exists(local_path + "/" + current_file_name + "_video.avi"):
        os.remove(local_path + "/" + current_file_name + "_video.avi")

    if os.path.exists(local_path + "/" + current_file_name + "_video2.avi"):
        os.remove(local_path + "/" + current_file_name + "_video2.avi")

    if os.path.exists(local_path + "/" + current_file_name + "_AV.avi"):
        os.remove(local_path + "/" + current_file_name + "_AV.avi")

    if os.path.exists(local_path + "/" + current_file_name + "_AV2.avi"):
        os.remove(local_path + "/" + current_file_name + "_AV2.avi")


# Function to read Sentences.txt and return all sentences in a list
def get_sentences():
    with open("roman_urdu_sentences.txt") as file:
        lines = [line.rstrip() for line in file]

    return lines


# Function to return string with spaces replaced with underscore
def remove_space(str):
    a = str
    a1 = ""
    for i in range(len(a)):
        if a[i] == ' ':
            a1 = a1 + '_'
        else:
            a1 = a1 + a[i]
    return a1


import wave
import numpy as np


def read_audio_file(audio_file_name):
    rate, data = read(audio_file_name)
    # wav_obj = wave.open(audio_file_name, 'rb')
    # Getting the sampling rate
    # sample_freq = wav_obj.getframerate()
    # Getting Number of individual frames
    n_samples = wav_obj.getnframes()
    # Getting duration of audio file
    t_audio = n_samples / sample_freq
    # Getting number of channels of sound
    n_channels = wav_obj.getnchannels()
    # Getting amplitude of wave at each frame
    signal_wave = wav_obj.readframes(n_samples)
    # To get signal values from this, we have to turn to numpy

    signal_array = np.frombuffer(signal_wave, dtype=np.int16)

    # Before we get to plotting signal values, we need to calculate the time at which each sample is taken.
    # This is simply the total length of the track in seconds, divided by the number of samples
    #  We can use linspace() from numpy to create an array of timestamps

    times = np.linspace(0, n_samples / sample_freq, num=n_samples)

    return [data, rate, signal_array, times]


# Prompt speaker to record again or proceed further
# (Returns True(next), False(prev))
def redo_flag_input():
    inp = ""

    while (inp != "y" and inp != "Y" and inp != "n" and inp != "N"):
        inp = input("\n Proceed to Next Sentence? (Y = next, N = re-record)")

    if (inp == "Y" or inp == "y"):
        return False  # redo flag = false
    else:
        return True  # redo flag = true


# Function to record a sentence and save it
def sentence_record_AV(speaker_id, current_sentence):
    new_dir = "./" + str(speaker_id) + "/" + remove_space(current_sentence)
    local_path = os.getcwd()
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

    current_file_name = new_dir + "/"  # + current_sentence

    file_manager()

    sent_display = current_sentence

    start_AVrecording()

    time.sleep(3.5)

    stop_AVrecording()
    print
    "Done"

    AudioManip.display_audio_amp_graph(current_file_name + "_audio.wav")


if __name__ == "__main__":

    # speaker_id = input("\n Please Enter a new speaker ID : ")

    speaker_id = 1

    sentence_list = get_sentences()  # Getting list of sentences

    # Looping over all sentences (108 total)
    for i in range(107, len(sentence_list)):

        # Flag to re-record a falsely spoken sentence
        redo_flag = True

        # Loop to rerun recording
        while (redo_flag == True):
            print("NEXT SENTENCE  " + str(i) + " : " + sentence_list[
                i])  # Displaying the sentence to be spoken on console

            inp = ' '
            while inp != 'g':
                inp = input("\nHit ENTER to start Recording next Sentence....")


            current_sentence = sentence_list[i]

            #sentence_record_AV(speaker_id, current_sentence)

            #--------------------------------------------------------------

            new_dir = "./" + str(speaker_id) + "/" + remove_space(current_sentence)
            local_path = os.getcwd()
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)

            current_file_name = new_dir + "/"  # + current_sentence

            file_manager()

            sent_display = current_sentence

            start_AVrecording()

            time.sleep(3.5)

            stop_AVrecording()
            print
            "Done"

            AudioManip.display_audio_amp_graph(current_file_name + "_audio.wav")
           # ------------------------------------------------

            print("\nVIDEO RECORDED !\n")

            # Prompting and taking input of Redo flag
            redo_flag = redo_flag_input()

print("MAKE COPY OF VIDEOS AND CHANGE ID")


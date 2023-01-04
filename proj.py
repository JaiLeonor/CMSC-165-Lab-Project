import cv2 
import numpy as np
from moviepy.editor import *

# resolution of the video
size = (1280, 720)

# all the videos that will be joined together
videos = [
    "Shot 1 - Mama.mp4", 
    "Shot 2 - Mama.mp4",
    "Shot 2 - Bobbie.mp4",
    "Shot 5 - Mama.mp4", 
    "Shot 6 - Gabbie.mp4",
    "Shot 7 - Teddie.mp4",
    "Shot 10 - Gabbie.mp4", 
    "Shot 12 - Bobbie.mp4",
    "Shot 13 - Alex.mp4",
    "Shot 14 - Gabbie.mp4", 
    "Shot 15 - Alex.mp4",
    "Shot 16 - Bobbie.mp4",
    "Shot 17 - Mama.mp4", 
    "Shot 18 - Bobbie.mp4",
    "Shot 22 - Mama.mp4",
    "Shot 24 - Bobbie.mp4",
    "Shot 25 - Teddie.mp4",
    "Shot 26 - Bobbie.mp4", 
    "Shot 27 - Teddie.mp4",
]

# FOR MANY BG SHOTS ===============
# all the background images to be used
# images = [
    # "house.mp4", 
    # "house.mp4",
    # "house.mp4",
    # "house.mp4", 
    # "house.mp4",
    # "house.mp4",
    # "house.mp4", 
    # "house.mp4",
    # "house.mp4",
    # "house.mp4", 
    # "house.mp4",
    # "house.mp4",
    # "house.mp4", 
    # "house.mp4",
    # "house.mp4",
    # "house.mp4",
    # "house.mp4",
    # "house.mp4", 
    # "house.mp4",
# ] 
# =================================

# FOR SINGLE BG SHOT ==============
# bg_video = cv2.VideoCapture("single_bg.mp4")
# =================================

# open the final video where all frames will be written in
processed_video = cv2.VideoWriter("processed_video.avi", cv2.VideoWriter_fourcc(*"MJPG"), 30.0, size)

# for each video do stuffs
# range is the number of shots
for shot in range(len(videos)):
    # get the current video
    current_video = cv2.VideoCapture(videos[shot])
    # FOR MANY BG SHOTS ===============
    bg_video = cv2.VideoCapture("house.mp4")
    # =================================

    # while the current video is opened
    while current_video.isOpened():
        # get the current frames
        ret1, frame = current_video.read()
        ret2, image = bg_video.read()

        # if no more frames, break
        if not ret1:
            current_video.release()
            # FOR MANY BG SHOTS ===============
            bg_video.release()
            # =================================
            break

        # resize the frame and bg to same size
        frame = cv2.resize(frame, size)
        image = cv2.resize(image, size)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # specify upper and lower thresholds
        if videos[shot] == "Shot 1 - Mama.mp4" or videos[shot] == "Shot 2 - Mama.mp4" or videos[shot] == "Shot 5 - Mama.mp4" or videos[shot] == "Shot 17 - Mama.mp4" or videos[shot] == "Shot 22 - Mama.mp4": 
          u_green = np.array([102, 255, 255])
          l_green = np.array([37, 60, 72])
        elif videos[shot] == "Shot 7 - Teddie.mp4" or videos[shot] == "Shot 25 - Teddie.mp4" or videos[shot] == "Shot 27 - Teddie.mp4":
          u_green = np.array([104, 255, 255])
          l_green = np.array([44, 23, 80])
        else: 
          u_green = np.array([102, 255, 255])
          l_green = np.array([50, 80, 15])

        # get the mask with Gaussian blur to soften edges 
        mask = cv2.inRange(hsv, l_green, u_green)
        mask = cv2.GaussianBlur(mask, (5, 5), 0)

        # ADDING BG IMAGE 
        # METHOD 1 ============
        frame[mask != 0] = [0,0,0]
        image[mask == 0] = [0,0,0]
        f = frame + image
        # =====================

        # METHOD 2 ============
        # bg = cv2.bitwise_and(frame, frame, mask = mask)
        # f = frame - bg
        # f = np.where(f == 0, image, f)
        # =====================
        
        # write the current frame to the final video 
        processed_video.write(f)

processed_video.release()
cv2.destroyAllWindows()

# get the processed video
processed_video = VideoFileClip("processed_video.avi")

# FOR SINGLE BG SHOT ==============
# # get the audio file
# bg_audio = AudioFileClip("single_bg.mp4")
# # set the audio file of the processed video
# # subclip gets only the first 0 to 3 seconds
# final_video = processed_video.set_audio(bg_audio.subclip(0,4))
# =================================

# FOR MANY BG SHOTS ===============
# concatenate all the audio from the video clips
bg_audio = concatenate_audioclips([AudioFileClip(c) for c in videos])
# set the audio file of the processed video
final_video = processed_video.set_audio(bg_audio)
# =================================

# save the video and the audio
final_video.write_videofile("final_video.mp4")
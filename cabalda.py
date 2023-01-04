import cv2 
import numpy as np

# resolution of the video
size = (1280, 720)

# all the videos that will be joined together
videos = [
    "shot6.mp4", 
    "shot7.mp4",
]

# all the background images to be used
images = [
    "bg_shot6.jpeg",
    "bg_shot7.jpg",
]

# open the final video where all frames will be written in
final_video = cv2.VideoWriter("final_video.avi", cv2.VideoWriter_fourcc(*"MJPG"), 30.0, size)

# for each video do stuffs
# range is the number of shots
for shot in range(len(videos)):
    # get the current video
    current_video = cv2.VideoCapture(videos[shot])
    image = cv2.imread(images[shot])

    # while the current video is opened
    while current_video.isOpened():
        # get the current frame
        ret, frame = current_video.read()

        # if no more frames, break
        if not ret:
            break

        # resize the frame and bg to same size
        frame = cv2.resize(frame, size)
        image = cv2.resize(image, size)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # specify upper and lower thresholds
        u_green = np.array([102, 255, 255])
        l_green = np.array([50, 80, 15])

        # get the mask with Gaussian blur to soften edges 
        mask = cv2.inRange(hsv, l_green, u_green)
        mask = cv2.GaussianBlur(mask, (5, 5), 0)

        # ADDING BG IMAGE 
        # METHOD 1 ============
        # frame[mask != 0] = [0,0,0]
        # image[mask == 0] = [0,0,0]
        # f = frame + image
        # =====================

        # METHOD 2 ============
        bg = cv2.bitwise_and(frame, frame, mask = mask)
        f = frame - bg
        f = np.where(f == 0, image, f)
        # =====================
        
        # write the current frame to the final video 
        final_video.write(f)

        # cv2.imshow("video", frame)
        # cv2.imshow("mask", mask)
        # cv2.imshow("bg", bg)
        # cv2.imshow("f", f)

        # if cv2.waitKey(25) == 27:
        #     break

final_video.release()
cv2.destroyAllWindows()
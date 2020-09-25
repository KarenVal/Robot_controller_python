"""Classes and functions for image processing"""
from imutils.video import VideoStream
import imutils
import numpy as np
import time
import cv2
import matplotlib.pyplot as plt
import os
from os import listdir

# Threshold of blue in HSV space used to recognize a robot or a ball
lower_blue = np.array([35, 140, 60])
upper_blue = np.array([255, 255, 180])


class Symbol:
    def __init__(self, img, name):
        self.img = img
        self.name = name
        self.refKeypoints = None
        self.refDescriptors = None
        self.refMatches = None


def import_reference_images():
    """Lets see if its really the need to use reference images"""
    symbols = []
    my_path = os.getcwd()
    my_path = my_path.replace('DIP_drivers', 'references\\')
    symbols_list = [f for f in listdir(my_path) if '.jpg' in str(f)]

    for image in symbols_list:
        path = my_path + image
        gray_image = cv2.imread(path, 0)
        ret, gray_image = cv2.threshold(gray_image, 100, 255, cv2.THRESH_TRUNC)

        img = Symbol(gray_image, image)
        symbols.append(img)
    return symbols


def normalize_image():
    return


def look_for_reference_image(image):
    """First attempt to get the robot number will use count of corners instead of reference images """
    match_list = []
    thresh = 8
    final_value = -1
    references = import_reference_images()
    # Initialize the ORB detector algorithm
    orb = cv2.ORB_create()

    # Now detect the keypoints and compute
    # the descriptors for the query image
    imgKeypoints, imgDescriptors = orb.detectAndCompute(image, None)
    try:
        for ref in references:
            # Now detect the keypoints and compute
            # the descriptors for the train image
            ref.refKeypoints, ref.refDescriptors = orb.detectAndCompute(ref.img, None)

            # Initialize the Matcher for matching
            # the keypoints and then match the
            # keypoints
            matcher = cv2.BFMatcher()
            matches = matcher.knnMatch(imgDescriptors, ref.refDescriptors, k=2)

            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    ref.refMatches.append([m])

            match_list.append(len(ref.refMatches))
    except:
        pass
    if len(match_list) != 0:
        if max(match_list) > thresh:
            final_value = match_list.index(max(match_list))

    return references[final_value].name


def calculate_distance_between_2_objects():
    return


def get_object_center():
    return


def get_object_position_in_field():
    return


def get_roi_from_webcam():
    return


if __name__ == '__main__':
    # Start video reading
    vs = VideoStream(src=0).start()

    # Allow the camera or video file to warm up
    time.sleep(2.0)

    # Start camera until user press q or close program
    while True:
        # grab the current frame
        frame = vs.read()

        # handle the frame
        # frame = frame[1]

        # resize the frame, blur it, and convert it to the HSV
        # color space
        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # construct a mask for the color "blue", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c_array = []

            # c = max(cnts, key=cv2.contourArea)
            for c in cnts:
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                c_array.append((x, y, radius, center))

            # only proceed if the radius meets a minimum size
            for c in c_array:
                x, y, radius, center = c
                # Get radius value
                if radius > 20:
                    height, width, channels = frame.shape
                    # Draw rectangle around roi
                    sum_value = int(radius)
                    top_x = (int(x) - sum_value) if (x - sum_value > 0) else 0
                    top_y = (int(y) - sum_value) if (y - sum_value > 0) else 0

                    bottom_x = (int(x) + sum_value) if (x + sum_value < width) else width
                    bottom_y = (int(y) + sum_value) if (y + sum_value < height) else height
                    cv2.rectangle(frame, (top_x, top_y), (bottom_x, bottom_y), (0, 255, 255), 2)

                    # Rectangled ROI
                    rect_image = frame[top_y: bottom_y, top_x: bottom_x]
                    gray = cv2.cvtColor(rect_image, cv2.COLOR_BGR2GRAY)
                    ref_name = str(look_for_reference_image(gray))
                    cv2.putText(frame, ref_name, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)

                    # draw the matches to the final image
                    # containing both the images the drawMatches()
                    # function takes both images and keypoints
                    # and outputs the matched query image with
                    # its train image
                    # final_img = cv2.drawMatchesKnn(gray, imgKeypoints, referencia, refKeypoints, good, None, flags=2)
                    # cv2.imshow("Referencia", final_img)

        # show the frame to our screen
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break

    # Stop camera
    vs.stop()

    # close all windows
    cv2.destroyAllWindows()

    print("Done")

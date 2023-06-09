#!/usr/bin/python
import argparse
import os
import random
import glob

import cv2
import imutils
import numpy as np

from face_recognition import detect_landmarks


# Check if a point is inside a rectangle
def rect_contains(rectangle, point):
    if point[0] < rectangle[0]:
        return False
    elif point[1] < rectangle[1]:
        return False
    elif point[0] > rectangle[2]:
        return False
    elif point[1] > rectangle[3]:
        return False
    return True


# Draw a point
def draw_point(img, p, color):
    cv2.circle(img, p, 2, color, cv2.FILLED, cv2.LINE_AA, 0)


# Draw delaunay triangles
def draw_delaunay(img, subdiv, delaunay_color):
    triangle_list = subdiv.getTriangleList()
    size = img.shape
    r = (0, 0, size[1], size[0])

    for t in triangle_list:

        pt1 = (int(t[0]), int(t[1]))
        pt2 = (int(t[2]), int(t[3]))
        pt3 = (int(t[4]), int(t[5]))

        if rect_contains(r, pt1) and rect_contains(r, pt2) and rect_contains(r, pt3):
            cv2.line(img, pt1, pt2, delaunay_color, 1, cv2.LINE_AA, 0)
            cv2.line(img, pt2, pt3, delaunay_color, 1, cv2.LINE_AA, 0)
            cv2.line(img, pt3, pt1, delaunay_color, 1, cv2.LINE_AA, 0)

def delaunay_triangulation(img, points):
    # Define window names
    win_delaunay = "Delaunay Triangulation"

    # Turn on animation while drawing triangles
    animate = False
    # Turn off landmark drawing
    draw_landmarks = True

    # Define colors for drawing.
    delaunay_color = (255, 255, 255)
    points_color = (0, 0, 255)

    # Keep a copy around
    img_orig = img.copy()

    # Rectangle to be used with Subdiv2D
    size = img.shape
    rect = (0, 0, size[1], size[0])

    # Create an instance of Subdiv2D
    subdiv = cv2.Subdiv2D(rect)

    # Insert points into subdiv
    for p in points:
        subdiv.insert(p)

        # Show animation
        if animate:
            img_copy = img_orig.copy()
            # Draw delaunay triangles
            draw_delaunay(img_copy, subdiv, (255, 255, 255))
            cv2.imshow(win_delaunay, img_copy)
            cv2.waitKey(100)

    # Draw delaunay triangles
    draw_delaunay(img, subdiv, delaunay_color)
    # Show results
    # cv2.imshow(win_delaunay, img)

    # Draw points
    if draw_landmarks:
        for p in points:
            draw_point(img, p, points_color)

    # Show results
    #cv2.waitKey(0)

    return img

def main():

    # Read the input image
    
    files = glob.glob(os.path.join(args.directory, '*.jpg'))
    files.sort(key=os.path.getmtime)  

    for filename in files:

        img_path = os.path.join(os.path.dirname(__file__), filename)
        assert os.path.exists(img_path)

        img = cv2.imread(img_path, 1)

        # Resize image keeping aspect-ratio to ensure no overflow in` visualization
        img = imutils.resize(img, width=800)
        

        # Detect landmarks using model
        _, landmarks = detect_landmarks(img)

        # Compute and draw triangulation
        img_delaunay = delaunay_triangulation(img, landmarks)

        # Save results in files
        # file_name = os.path.splitext(img_path)[0]
        # file_extension = os.path.splitext(img_path)[1]
        if not cv2.imwrite((filename), img_delaunay):
            raise Exception("could not write image")

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='Process image for facial recognition analysis and visualization.')
    #parser.add_argument('--image', help='image to process', required=True)
    parser.add_argument('--directory', required=True)
    args = parser.parse_args()

    # Call main function
    main()


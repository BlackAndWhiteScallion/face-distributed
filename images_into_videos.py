import cv2
import numpy as np
import glob
import os
import argparse

def i2v (video, directory):
    img_array = []
    files = glob.glob(os.path.join(directory, '*.jpg'))
    files.sort(key=os.path.getmtime)
    for filename in files:
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
     
    out = cv2.VideoWriter(os.path.join(directory, video),cv2.VideoWriter_fourcc(*'VP80'), 25, size)
 
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

def main():
    video = args.video
    directory = args.directory
    i2v (video, directory)    

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='Process image for facial recognition analysis and visualization.')
    parser.add_argument('--video', required=True)
    parser.add_argument('--directory', required=True)
    args = parser.parse_args()

    main()

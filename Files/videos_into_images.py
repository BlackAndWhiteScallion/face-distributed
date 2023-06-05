import cv2
import sys
import argparse
import os

def v2i (video, directory):
    capture = cv2.VideoCapture(video) 
    frameNr = 0
    while (True):
            success, frame = capture.read()
            if not success:
                break
            cv2.imwrite(os.path.join(directory, str(frameNr)+'.jpg'), frame)
            frameNr = frameNr+1
    capture.release()

def main():
    video = args.video
    directory = args.directory
    v2i (video, directory)

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='Process image for facial recognition analysis and visualization.')
    parser.add_argument('--video', required=True)
    parser.add_argument('--directory', required=True)
    args = parser.parse_args()

    main()

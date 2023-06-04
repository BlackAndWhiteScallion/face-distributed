import glob
import os


files = glob.glob("output/*.jpg")
files.sort(key=os.path.getmtime)



import sys
import os
import subprocess
import uuid
import time
import psycopg2
from flask import Flask, flash, request, redirect, url_for, render_template, send_file, send_from_directory
import urllib.request
from werkzeug.utils import secure_filename
import cv2

app = Flask(__name__)
app.secret_key = "secret key"

# Define the route for the index page
@app.route('/')
def index():
    return render_template('index.html');
    #with open('index.html', 'r') as file:
    #    return file.read()

# Define the route for processing the uploaded video
@app.route('/process', methods=['POST'])
def process():
    # Create a unique directory to store the uploaded video and processed frames
    unique_id = str(uuid.uuid4())
    #unique_id = "1"  
    upload_dir = os.path.join("uploads", unique_id)
    os.makedirs(upload_dir, exist_ok=True)

    # Save the uploaded video file
    video_file = request.files['selfieVideo']
    video_path = os.path.join(upload_dir, video_file.filename)
    video_file.save(video_path)

    conn = psycopg2.connect("dbname = 'pyapp' user='student' password='student'")
    cur = conn.cursor()
    cur.execute('INSERT INTO data(workerID, videoID, sendTime, frameNumber) VALUES(%s, %s, %s, %s);',
    (1, unique_id, int(time.perf_counter()), int(cv2.VideoCapture(video_path).get(cv2.CAP_PROP_FRAME_COUNT))))
    conn.commit()
    
    # Divide video into images using your Python code
    subprocess.check_call(['python3', 'videos_into_images.py', '--video', video_path, '--directory', upload_dir])
    # Apply Delaunay triangles to the images using your Python code
    subprocess.check_call(['python3', 'delaunay.py', '--directory', upload_dir])
    
    # Combine processed images into a video using your Python code
    subprocess.check_call(['python3', 'images_into_videos.py', '--directory', upload_dir, '--video', 'processed_video.webm'])

    # Define the path for the processed video
    processed_video_path = os.path.join(unique_id, 'processed_video.webm')
    
    cur.execute('UPDATE data SET receiveTime = %s WHERE videoID = %s', (int(time.perf_counter()), unique_id))
    conn.commit()
    
    cur.execute("SELECT workerID, videoID, sendTime, receiveTime, frameNumber FROM data")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('finished.html', filename = processed_video_path, data = data)

@app.route('/display/<path:filename>')
def display_video(filename):
    return send_from_directory('uploads', filename)	
    
@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory('uploads', filename, as_attachment=True)

if __name__ == '__main__':
    #app.run(debug=True, port = 9998, host="172.20.222.131")
    app.run(debug=True, port = 9998)

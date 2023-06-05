from flask import Flask, request, send_file
import os
import subprocess
import uuid

app = Flask(__name__)

# Define the route for the index page
@app.route('/')
def index():
    with open('index.html', 'r') as file:
        return file.read()



# Define the route for processing the uploaded video
@app.route('/process', methods=['POST'])
def process():
    # Create a unique directory to store the uploaded video and processed frames
    unique_id = str(uuid.uuid4())
    upload_dir = os.path.join("uploads", unique_id)
    os.makedirs(upload_dir)

    # Save the uploaded video file
    video_file = request.files['selfieVideo']
    video_path = os.path.join(upload_dir, video_file.filename)
    video_file.save(video_path)

    # Divide video into images using your Python code
    subprocess.check_call(['python3', 'videos_into_images.py', '--video', video_path, '--directory', upload_dir])

    # Apply Delaunay triangles to the images using your Python code
    subprocess.check_call(['python3', 'delaunay.py', '--directory', upload_dir])

    # Combine processed images into a video using your Python code
    subprocess.check_call(['python3', 'images_into_videos.py', '--directory', upload_dir, '--video', 'processed_video.avi'])

    # Define the path for the processed video
    processed_video_path = os.path.join(upload_dir, 'processed_video.avi')

    # Return the processed video for download
    return send_file(processed_video_path, as_attachment=True)

if __name__ == '__main__':
    app.run()

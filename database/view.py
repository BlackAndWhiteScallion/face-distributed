import sys
import os
import subprocess
import uuid
import time
import psycopg2
from flask import Flask, flash, request, redirect, url_for, render_template, send_file, send_from_directory
import urllib.request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "secret key"

@app.route('/')
def index():
    # Fetch data from the PostgreSQL database
    conn = psycopg2.connect("dbname = 'pyapp' user='student' password='student'")
    cursor = conn.cursor()
    cursor.execute("SELECT workerID, videoID, sendTime, receiveTime, frameNumber FROM data")
    data = cursor.fetchall()

    # Render the HTML page with the data
    return render_template('table.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, port = 2945)

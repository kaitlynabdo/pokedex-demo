#!/bin/env python3
import cv2
import numpy as np
from PIL import Image
from flask import Flask, send_file, render_template, request, jsonify, Response
from flask_socketio import SocketIO, emit
import torch
import threading
import io
from io import BytesIO
import base64
import time
import os
import eventlet
import pandas

# Model
model = torch.hub.load('yolov5', 'custom', path='/app/best.pt', source='local')

app = Flask(__name__)

video_path = '/app/pokemon3.mp4'
stream = cv2.VideoCapture(video_path)
results = None
results_lock = None
name = None
stats = None 
row = None
type1 = None 
hp = None
attack = None
defense = None
speed = None

def get_frame():
    while True:
        global results
        if not results_lock==True:
            for im in results.ims:
                buffered = BytesIO()
                im_base64 = Image.fromarray(im)
                im_base64.save(buffered, format="JPEG")
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffered.getbuffer().tobytes() + b'\r\n')
            time.sleep(0.2)

def read_video():
    global cap, stream, results
    while (stream.isOpened()):
        try:
            ret, frame = stream.read()
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results_lock = True
            results = model(image_rgb)
            results.render()  # updates results.ims with boxes and labels
            results_lock = None
            time.sleep(0.05)

        except:
            continue

@app.route('/pokedex')
def get_image():
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stats')
def get_stats():
    global name
    global stats
    global row
    global type1
    global hp
    global attack
    global defense
    global speed
    stats = pandas.read_csv('/app/stats.csv')   
    try:
        name = str(results.pandas().xyxy[0]['name'][0])
        row = stats.loc[stats['Name'] == name].values.tolist()
        type1 = str(row[0][3])
        hp = str(row[0][6])
        attack = str(row[0][7])
        defense = str(row[0][8])
        speed = str(row[0][11])
        return render_template('stats.html', name=name, type1=type1, hp=hp, attack=attack, defense=defense, speed=speed) 

    except:
        return "No pokemons in sight..."

@app.route('/')
def index():
    return """
    <body style="background: black;">
        <div style="width: 240px; margin: 0px auto;">
            <img src="/mjpeg" />
        </div>
    </body>
    """

if __name__ == '__main__':
    t=threading.Thread(target=read_video)
    t.start()
    app.run(host='0.0.0.0', port=5000, threaded=True)

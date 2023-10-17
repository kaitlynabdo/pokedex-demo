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

app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.route('/')
def render_index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

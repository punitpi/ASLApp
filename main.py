#!/usr/bin/env python
#
# Project: Video Streaming with Flask
# Author: Log0 <im [dot] ckieric [at] gmail [dot] com>
# Date: 2014/12/21
# Website: http://www.chioka.in/
# Description:
# Modified to support streaming out with webcams, and not just raw JPEGs.
# Most of the code credits to Miguel Grinberg, except that I made a small tweak. Thanks!
# Credits: http://blog.miguelgrinberg.com/post/video-streaming-with-flask
#
# Usage:
# 1. Install Python dependencies: cv2, flask. (wish that pip install works like a charm)
# 2. Run "python main.py".
# 3. Navigate the browser to the local webpage.
from flask import Flask, render_template, Response, jsonify, redirect, request, url_for
from camera import VideoCamera
import base64
app = Flask(__name__)

camera =  VideoCamera()
@app.route('/')
def index():
    return render_template('index.html')



def gen():
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/move_forward', methods=['GET', 'POST'])
def move_forward():
        
        jsdata = request.get_data() 
        jpg_recovered = base64.decodestring(jsdata)
        f = open("temp.jpg", "w")
        f.write(jpg_recovered)
        f.close()
        prediction_message, score = camera.get_predictions()
        return jsonify({'value': prediction_message})


if __name__ == '__main__':
    app.run(host='localhost', debug=True)

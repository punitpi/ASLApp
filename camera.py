import cv2
import pickle
import numpy as np
import os
import sqlite3
import tensorflow as tf
import sys
from keras.models import load_model


class VideoCamera(object):
    def get_frame(self):
        success, image = self.video.read()

        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        img = cv2.flip(image, 1)
        x1, y1, x2, y2 = 100, 100, 300, 300
        cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,0), 2)

        
        img_cropped = img[y1:y2, x1:x2]
        self.data = cv2.imencode('.jpg', img_cropped)[1].tostring()

        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()

    def get_predictions(self):
        with tf.gfile.FastGFile("logs/trained_graph.pb", 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')

        with tf.Session() as sess:
            image_path = "temp.jpg"
            image_data = tf.gfile.FastGFile(image_path, 'rb').read()
            os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
            label_lines = [line.rstrip() for line
                   in tf.gfile.GFile("logs/trained_labels.txt")]
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
            # Read the image_data
            # Loads label file, strips off carriage return
            predictions = sess.run(softmax_tensor, \
                {'DecodeJpeg/contents:0': image_data})

            # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

            max_score = 0.0
            res = ''
            for node_id in top_k:
                human_string = label_lines[node_id]
                score = predictions[0][node_id]
                if score > max_score:
                    max_score = score
                    res = human_string
            return res, max_score


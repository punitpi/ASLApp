import cv2
import pickle
import numpy as np
import os
import sqlite3
import tensorflow as tf
import sys
from keras.models import load_model
from PIL import Image


class VideoCamera(object):
    def get_predictions(self):
        with tf.gfile.FastGFile("logs/trained_graph.pb", 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')

        with tf.Session() as sess:
            image_path = "temp.jpg"
            crop(image_path, image_path)
            image_data = tf.gfile.FastGFile(image_path, 'rb').read()
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
            label_lines = [line.rstrip() for line
                           in tf.gfile.GFile("logs/trained_labels.txt")]
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
            # Read the image_data
            # Loads label file, strips off carriage return
            predictions = sess.run(softmax_tensor,
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

def crop(image_path, saved_location):
    """
    @param image_path: The path to the image to edit
    @param coords: A tuple of x/y coordinates (x1, y1, x2, y2)
    @param saved_location: Path to save the cropped image
    """
    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop((0, 0, 200, 200))
    cropped_image.save(saved_location)


import os
from flask import jsonify, request
import flask
import requests
import pandas as pd
#from sklearn.externals import joblib
import joblib
import mysql.connector as sql
#from pyspark import SparkContext
#from pyspark.sql import SQLContext

import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'c:\\Program Files\\Tesseract-OCR\\tesseract.exe'

app = flask.Flask(__name__)

@app.route('/')
def index():
	return flask.render_template('index.html')
	
	
@app.route("/image", methods=['GET', 'POST'])
def predict():
	if flask.request.method == 'GET':
		img = cv2.imread('static/img/more.png')
		crop_img = img[150:220, 800:1200]
		text = pytesseract.image_to_string(crop_img)
	if flask.request.method == 'POST':
		x = int(request.values["x"])
		y = int(request.values["y"])
		w = int(request.values["w"])
		h = int(request.values["h"])
		img = cv2.imread('static/img/more.png')
		crop_img = img[y:y + h, x:x + w]
		text = pytesseract.image_to_string(crop_img)
	
	return flask.jsonify(text)

if __name__ == '__main__':
	app.debug=True
	app.run()

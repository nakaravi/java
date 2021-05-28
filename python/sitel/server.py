"""Filename: server.py
"""


import os
#from flask import Flask, jsonify, request
import flask
from flask_cors import CORS, cross_origin
import requests
import pandas as pd
#from sklearn.externals import joblib
import mysql.connector as sql
from pyspark import SparkContext
from pyspark.sql import SQLContext

app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin()
def index():
	return flask.render_template('index.html')


@app.route("/upload", methods=['GET', 'POST'])
@cross_origin()
def upload():
	if flask.request.method == 'POST':
		#print(flask.request.files['file'])
		f = flask.request.files['file']
		f.save('data.xlsx')
		return flask.jsonify({'result':'success', 'data':'Successfully Uploaded !', 'filename':f.filename})
		#data_xls = pd.read_excel(f)
		#return data_xls.to_html()
	return '''
    <!doctype html>
    <title>Upload an excel file</title>
    '''
@app.route("/read", methods=['GET', 'POST'])
@cross_origin()
def read():
	if flask.request.method == 'POST' or flask.request.method == 'GET':
		data_xls = pd.read_excel('data.xlsx')
		return data_xls.to_json(orient='records')
		return flask.jsonify({'result':'success', 'data':'Successfully Uploaded !', 'filename':f.filename})
		
if __name__ == '__main__':
	app.debug=True
	app.run()

	

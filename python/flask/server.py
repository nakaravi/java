"""Filename: server.py
"""


import os
#from flask import Flask, jsonify, request
import flask
import pandas as pd
from sklearn.externals import joblib
import mysql.connector as sql
from pyspark import SparkContext
from pyspark.sql import SQLContext

app = flask.Flask(__name__)

@app.route('/')
def index():
	return flask.render_template('index.html')
	
	
@app.route("/products", methods=['GET'])
def predict():
    if flask.request.method == 'GET':
        try:
			db_connection = sql.connect(host='localhost', database='api', user='root', password='')
			db_cursor = db_connection.cursor()
			db_cursor.execute('SELECT * FROM products')
			print(db_cursor)
			table_rows = db_cursor.fetchall()
			
			#below method 1
			
			df = pd.DataFrame(table_rows)
			json = df.reset_index().to_json(orient='table')#orient ='table','records','split','table')
			return json
			
			#below method 2
			#json = []
			#for result in table_rows:
			#	json.append({'id':result[0],'name':result[1],'description':result[2],'price':float(result[3]),'created':result[4], 'modified':result[5]})
			
			#return flask.jsonify(json)
        except ValueError:
            return flask.jsonify("Query error")
			

@app.route("/product", methods=['GET'])
def product():
    if flask.request.method == 'GET':
		try:
			dataframe_mysql = SQLContext.read.format("jdbc").options( url="jdbc:mysql://localhost/mysql",driver = "com.mysql.jdbc.Driver",dbtable = "api",user="root", password="").load()
			dataframe_mysql.show()
		except ValueError:
			return flask.jsonify("Query Error.")
		
if __name__ == '__main__':
	app.debug=True
	app.run()

	

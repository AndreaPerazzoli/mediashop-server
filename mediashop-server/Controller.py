import datetime
import json
import logging

import decimal
from flask import jsonify
from flask import Flask, request
from Model import Model
import decimal
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
model = app.model = Model()


class MyEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, decimal.Decimal):
			return float(o)
		if isinstance(o, datetime.datetime):
			return o.isoformat()
		if isinstance(o, list):
			json_string = ""
			for a in o:
				json_string += json.JSONEncoder.default(self, a)
			return json_string
		return json.JSONEncoder.default(self, o)


@app.route('/getAllProducts')
def getAllProducts():
	'''Returns the entire list of products'''
	result = model.getProducts()



	return jsonify(result)  # render_template("query_result.html", result=result)



@app.route('/getProductById', methods=["POST"])
def getProductById():
	id = request.form["idProduct"]
	result = model.getProductById(id)

	return jsonify(result)


@app.route('/buyProductById', methods=["POST"])
def buyProductById():
	productId = request.form["productId"]
	paymentType = request.form["paymentType"]
	clientUsername = request.form["clientUsername"]
	clientIP = request.remote_addr

	result = model.buyProductWithId(productId, clientIP=clientIP, paymentType=paymentType,
	                                clientUsername=clientUsername)

	return jsonify(result)  # render_template("query_result.html", result=result)



if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

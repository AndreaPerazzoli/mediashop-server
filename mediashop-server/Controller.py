import logging
from flask import jsonify
from flask import Flask, request, render_template

from Model import Model

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
model = app.model = Model()


@app.route('/getAllProducts')
def getAllProducts():
	'''Returns the entire list of products'''
	result = model.getProducts()

	return  jsonify(result) #render_template("query_result.html", result=result)


@app.route('/getProductById', methods=["POST"])
def getProductById():
	id = request.form["idProduct"]
	result=model.getProductById(id)

	return jsonify(result) 

@app.route('/buyProductById', methods=["POST"])
def buyProductById():
	productId = request.form["productId"]
	paymentType = request.form["paymentType"]
	clientUsername = request.form["clientUsername"]
	clientIP = request.remote_addr


	result = model.buyProductWithId(productId, clientIP=clientIP, paymentType=paymentType, clientUsername=clientUsername)

	return jsonify(result) #render_template("query_result.html", result=result)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

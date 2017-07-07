
import logging
from flask import Flask, request, jsonify
from Model import Model

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
model = app.model = Model()


@app.route('/getAllProducts')
def getAllProducts():
	'''Returns the entire list of products'''
	result = model.getProducts()

	return jsonify(result)


@app.route('/getProductById', methods=["POST"])
def getProductById():
	id = request.form["id"]
	result = model.getProductById(id)

	return jsonify(result)



@app.route('/buyProductById', methods=["POST"])
def buyProductById():
	productId = request.form["id"]
	paymentType = request.form["paymentType"]
	clientUsername = request.form["client"]
	clientIP = request.remote_addr

	result = model.buyProductById(productId, clientIP=clientIP, paymentType=paymentType, clientUsername=clientUsername)

	return jsonify(result)


@app.route('/login', methods=["POST"])
def login():
	username = request.form["username"]
	password = request.form["password"]

	result = model.login(username,password)

	return jsonify(result)


@app.route('/register', methods=["POST"])
def registration():
	username = request.form["username"]
	password = request.form["password"]
	city = request.form["city"]
	fiscalCode = request.form["fiscalCode"]
	name = request.form["name"]
	surname = request.form["surname"]
	phone = request.form["phone"]
	mobilePhone = request.form["mobilePhone"]
	favouriteGenre = request.form["favouriteGenre"]

	result = model.registration(username,password,city,fiscalCode,name,surname,phone,mobilePhone, favouriteGenre)
	return jsonify(result)


@app.route('/searchProduct', methods=["POST"])
def search():

	subject = request.form["subject"]

	result = model.searchProductBy( subject)
	return jsonify(result)


@app.route('/searchProductByPrice', methods=["POST"])
def searchProductByPrice():
	minPrice = request.form["minPrice"]
	maxPrice = request.form["maxPrice"]

	result = model.searchProductByPrice(minPrice,maxPrice)
	return jsonify(result)

@app.route('/purchaseHistory')
def getPurchasedProducts():
	userId = request.form["username"]
	result = model.getPurchasedProducts(userId)
	return jsonify(result)



if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')


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
	numerOfProducts = request.form["quantity"]
	clientIP = request.remote_addr

	result = model.buyProductById(productId, clientIP, paymentType, clientUsername,numerOfProducts)

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

@app.route('/purchaseHistory', methods=["POST"])
def getPurchasedProducts():
	userId = request.form["username"]
	result = model.getPurchasedProducts(userId)
	return jsonify(result)


@app.route('/getTrackByProductId',methods=["POST"])
def getTrackByProductId():
	productId = request.form["productId"]
	result = model.getTrackBy(productId)
	return jsonify(result)

@app.route('/getAllProductsPreferredByUsername',methods=["POST"])
def getAllProductsPreferredByUsername():
	username = request.form["username"]
	result = model.getAllProductsPreferredByUsername(username)
	return jsonify(result)

# @app.route('/getProductByAttribute',methods=["POST"])
# def getProductByAttribute():
# 	attribute = request.form["attribute"]
# 	value = request.form["value"]
# 	result = model.getProductByAttribute(attribute, value)
# 	return jsonify(result)

@app.route('/getProductByGenre',methods=["POST"])
def getProductByGenre():
	genre = request.form["genre"]

	result = model.getProductByGenre(genre)
	return jsonify(result)

@app.route('/getProductBySoloist',methods=["POST"])
def getProductBySoloist():
	soloist = request.form["soloist"]

	result = model.getProductBySoloist(soloist)
	return jsonify(result)

@app.route('/getProductByBand',methods=["POST"])
def getProductByBand():
	bandName = request.form["bandName"]

	result = model.getProductByBand(bandName)
	return jsonify(result)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

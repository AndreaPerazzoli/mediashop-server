import logging
from flask import Flask, request, render_template

from Model import Model

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
model = app.model = Model()


@app.route('/getAllProducts')
def getAllProducts():
	'''Returns the entire list of products'''
	result = model.getProducts()
	return render_template("query_result.html", result=result)


@app.route('/getProductById', methods=["POST"])
def getProductById():
	id = request.form["idProduct"]
	result=model.getProductById(id)
	return render_template("query_result.html",result=result)
# @app.route('/home', methods="Post")
# def getProductId():
# 	request.form["productId"]
#
# 	model.buyProductWithId()

if __name__ == '__main__':
	app.run(debug=True)

import logging
from flask import Flask, request, render_template

from Model import Model

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
model = app.model = Model()


@app.route('/')
def homepage():
	'''Returns the entire list of products'''
	result = model.getProduct()
	return render_template("query_result.html", result=result)


if __name__ == '__main__':
	app.run(debug=True)

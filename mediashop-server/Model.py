from Datamapper import DM_PG


class Model:
	def __init__(self):
		self.datamapper = DM_PG()

	def __del__(self):
		self.datamapper.close()

	def getProducts(self):

		return self.datamapper.getProducts()

	def getProductById(self, id):
		return self.datamapper.getProductById(id)

	def buyProductWithId(self, productId, clientIP, paymentType, clientUsername):
		return self.datamapper.buyProductWithId(productId, clientIP, paymentType, clientUsername)

	def login(self, username, password):
		return self.datamapper.login(username, password)

	def registration(self, username, password, city, fiscalCode, name, surname, phone, mobilePhone, favouriteGenre):
		return self.datamapper.registration(username, password, city, fiscalCode, name, surname, phone, mobilePhone, favouriteGenre)
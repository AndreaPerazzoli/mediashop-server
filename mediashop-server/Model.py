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

	def buyProductById(self, productId, clientIP, paymentType, clientUsername):
		return self.datamapper.buyProductById(productId, clientIP, paymentType, clientUsername)

	def login(self, username, password):
		return self.datamapper.login(username, password)

	def registration(self, username, password, city, fiscalCode, name, surname, phone, mobilePhone, favouriteGenre):
		return self.datamapper.registration(username, password, city, fiscalCode, name, surname, phone, mobilePhone, favouriteGenre)

	def searchProductBy(self, attribute, subject):
		return self.datamapper.searchProductBy(attribute, subject)

	def searchProductByPrice(self, minPrice, maxPrice):
		return self.datamapper.searchProductByPrice(minPrice, maxPrice)

	def getPurchasedProducts(self, clientUsername):
		return self.datamapper.getPurchasedProducts(clientUsername)
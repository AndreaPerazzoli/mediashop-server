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

	def buyProductById(self, productId, clientIP, paymentType, clientUsername, numberOfProducts):
		return self.datamapper.buyProductById(productId, clientIP, paymentType, clientUsername, numberOfProducts)

	def login(self, username, password):
		return self.datamapper.login(username, password)

	def registration(self, username, password, city, fiscalCode, name, surname, phone, mobilePhone, favouriteGenre):
		return self.datamapper.registration(username, password, city, fiscalCode, name, surname, phone, mobilePhone, favouriteGenre)

	def searchProductBy(self, subject):
		return self.datamapper.searchProductBy( subject)

	def searchProductByPrice(self, minPrice, maxPrice):
		return self.datamapper.searchProductByPrice(minPrice, maxPrice)

	def getPurchasedProducts(self, clientUsername):
		return self.datamapper.getPurchasedProducts(clientUsername)

	def getTrackBy(self, productId):
		return  self.datamapper.getTrackBy(productId)

	def getAllProductsPreferredByUsername(self, username):
		return self.datamapper.getAllProductsPreferredByUsername(username)

	def getProductByGenre(self, genre):
		return self.datamapper.getProductByAttribute("main_genre",genre)

	def getProductBySoloist(self, soloist):
		return self.datamapper.getProductByAttribute("soloist", soloist)
	def getProductByBand(self, bandName):
		return self.datamapper.getProductByAttribute("bandName", bandName)

	def getProductByAttribute(self, attribute, value):
		return self.datamapper.getProductByAttribute(attribute, value)
from Datamapper import DM_PG


class Model:
	def __init__(self):
		self.datamapper = DM_PG()

	def __del__(self):
		self.datamapper.close()

	def getProduct(self):
		return self.datamapper.getProduct()

	def getProductById(self, id):
		return self.datamapper.getProductById(id)

	def buyProductWithId(self, productId, clientIP, paymentType, clientUsername):
		return self.datamapper.buyProductWithId(productId, clientIP, paymentType, clientUsername)

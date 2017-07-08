import json
from datetime import datetime
from decimal import Decimal
import time
import logging

import psycopg2.extras


class DM_PG():
	"""Data mapper verso PostgreSQL. Per semplicità, i parametri \
	di connessione sono attributi di classe: dovrebbero essere \
	scritti in un file esterno e caricati durante __init__."""

	__server = 'localhost'
	__db = 'postgres'
	__db4Log = ''
	__user = 'postgres'
	__pw = 'postgres'
	__dbCon = None
	__db4LogCon = None  # La connessione è condivisa!
	__nIstanze = 0

	@classmethod
	def __open(cls):
		if cls.__dbCon is None:
			try:
				cls.__dbCon = psycopg2.connect(host=cls.__server, database=cls.__db, user=cls.__user, password=cls.__pw)
				cls.__dbCon.set_session(autocommit=True)  # Connessione di lettura condivisa
				logging.info("Connection to database " + cls.__db + " created.")
			except psycopg2.OperationalError as err:
				logging.error("Error connecting to PostgreSQL DBMS at %s.\nDetails: %s.", cls.__server, err)
				cls.__dbCon = cls.__db4LogCon = None
				exit()
				# else:  # Questo else è del TRY
				#     try:
				#         cls.__db4LogCon = psycopg2.connect(host=cls.__server, database = cls.__db4Log, user=cls.__user, password=cls.__pw)
				#         cls.__db4LogCon.set_session(autocommit=True)
				#         # Connessione di scrittura condivisa
				#         logging.info("Connection to database " + cls.__db4Log + " created.")
				#     except psycopg2.OperationalError as err:
				#         logging.error("Error connecting to PostgreSQL DBMS at %s.\nDetails: %s.", cls.__server, err)
				#         cls.__dbCon = cls.__db4LogCon = None
				#         exit()
				return "New connection opened."
		return "Connection already opened."

	@classmethod
	def __close(cls):
		if cls.__nIstanze == 0 and cls.__dbCon is not None:
			cls.__dbCon.close()
			# cls.__db4LogCon.close()
			logging.info("Connection closed.")
			cls.__dbCon = None
		# cls.__dbCon = cls.__db4LogCon = None

	@classmethod
	def __cursor(cls):
		"""Ritorna un cursore che restituisce dict invece di tuple \ per ciascuna riga di una select."""
		return cls.__dbCon.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

	@classmethod
	def __cursor4log(cls):
		"""Ritorna un cursore per scrivere nel database \ cls.__db4Log."""
		return cls.__db4LogCon.cursor()

	def __init__(self):
		DM_PG.__open()
		DM_PG.__nIstanze += 1

	def close(self):
		self.__del__()

	def __del__(self):
		DM_PG.__nIstanze -= 1
		DM_PG.__close()


	def login(self, username, password):
		try:
			with DM_PG.__cursor() as cur:
				cur.execute(
					'SELECT *'
					'FROM Client C '
					'WHERE C.username = %s AND C.password = %s ', (username, password)

				)


				return list(cur)

		except psycopg2.Error as err:
			error_string = "Log in error.\nDetails:" + str(err)
			logging.error(error_string)
			return [{"error": error_string}]


	def registration(self, username, password, city, fiscalCode, name, surname, phone, mobilePhone, favouriteGenre):
		try:
			if mobilePhone == "" or str.lower(mobilePhone) == "null": mobilePhone = None
			if favouriteGenre == "" or str.lower(favouriteGenre) == "": favouriteGenre = None

			print(username, password, city, fiscalCode, name, surname, phone, mobilePhone, favouriteGenre)
			with DM_PG.__cursor() as cur:
				cur.execute(
					'INSERT INTO Client(username, password, city, fiscalCode, name, surname, phone, mobilePhone, favouriteGenre) '
					'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ',
					(username, password, city, fiscalCode, name, surname, phone, mobilePhone, favouriteGenre)
				)

			return [{"username": username, "password": password, "city":city, "fiscalCode": fiscalCode,
			"name": name, "surname":surname, "phone":phone, "mobilePhone":mobilePhone, "favouriteGenre": favouriteGenre}]
		except psycopg2.IntegrityError as ierr:
			error_string = "Registration error.\nDetails:" + str(ierr)
			logging.error(error_string)
			return [{"registered": 0}]
		except psycopg2.Error as err:
			error_string = "Registration error.\nDetails:" + str(err)
			logging.error(error_string)
			return [{"error": error_string}]


	def getProducts(self):
		try:
			with DM_PG.__cursor() as cur:
				cur.execute(
					'SELECT * '
					'FROM Product P '
					'LEFT JOIN Band B ON P.bandName = B.bandName '
					'LEFT JOIN Soloist S ON P.soloist = S.stagename '
					'LEFT JOIN Cover C ON C.product = P.id '


				)

				return list(cur)
		except psycopg2.Error as err:
			error_string = "Get error.\nDetails:" + str(err)
			logging.error(error_string)
			return [{"error": error_string}]

	def getTrackBy(self, productId):
		try:
			with DM_PG.__cursor() as cur:
				cur.execute(
					'SELECT T.title , T.track_order '
					'FROM Track T '
					'JOIN Product P ON T.product = P.id '
					'WHERE P.id = %s '
					'ORDER BY T.track_order',(productId,)
				)
				return list(cur)

		except psycopg2.Error as err:
			error_string = "Get error.\nDetails:" + str(err)
			logging.error(error_string)
			return [{"error": error_string}]

	def searchProductBy(self, subject):
		dictd = dict(like='%' + subject + '%')

		try:
			with DM_PG.__cursor() as cur:
				cur.execute(
					"SELECT * "
					"FROM Product P "
					"LEFT JOIN Cover C ON C.product = P.id "
					"WHERE P.description ILIKE %(like)s "
					"OR P.title ILIKE %(like)s "
					"OR P.soloist ILIKE %(like)s "
					"OR P.type ILIKE %(like)s "
					"OR P.bandName ILIKE %(like)s ESCAPE '='", dictd
				)

				return list(cur)
		except psycopg2.Error as err:
			error_string = "Search error.\nDetails:" + str(err)
			logging.error(error_string)
			return [{"error": error_string}]


	def searchProductByPrice(self, minPrice, maxPrice):
		minPrice = Decimal(minPrice)
		maxPrice = Decimal(maxPrice)
		try:
			with DM_PG.__cursor() as cur:
				cur.execute(
					"SELECT * "
					"FROM Product P "
					"LEFT JOIN Cover C ON C.product = P.id "
					"WHERE P.price BETWEEN %s AND %s ",(minPrice, maxPrice)
				)
				return list(cur)
		except psycopg2.Error as err:
			error_string = "Search error.\nDetails:" + str(err)
			logging.error(error_string)
			return [{"error": error_string}]


	def getProductById(self, id):
		try:
			with DM_PG.__cursor() as cur:
				cur.execute(
					'SELECT * '
					'FROM Product P '
					'WHERE id = %s', (id,)
				)

				return list(cur)
		except psycopg2.Error as err:
			error_string = "Get error.\nDetails:" + str(err)
			logging.error(error_string)
			return [{"error": error_string}]

			# search by attribute, value
	def getProductByAttribute(self, attribute, value):

		dic = dict(like='%' + value + '%')
		try:

			with DM_PG.__cursor() as cur:
				sql = "SELECT * FROM Product WHERE %s"%(attribute) +" ILIKE %(like)s ESCAPE '='"
				cur.execute(sql, dic)
				return list(cur)
		except psycopg2.Error as err:
			error_string = "Get error.\nDetails:" + str(err)
			logging.error(error_string)
		return [{"error": error_string}]

	# # ricerca per genre, soloist, bandName
	# def getProductByGenre(self, genre):
	# 	try:
	# 		with DM_PG.__cursor() as cur:
	#
	# 			cur.execute(
	# 				'SELECT * '
	# 				'FROM Product P '
	# 				'WHERE main_genre ilike %s', (genre,)
	# 			)
	# 			return list(cur)
	# 	except psycopg2.Error as err:
	# 		error_string = "Get error.\nDetails:" + str(err)
	# 		logging.error(error_string)
	# 	return [{"error": error_string}]
	#
	# def getProductBySoloist(self, soloist):
	# 	try:
	# 		with DM_PG.__cursor() as cur:
	#
	# 			cur.execute(
	# 				'SELECT * '
	# 				'FROM Product P '
	# 				'WHERE soloist ilike %s', (soloist,)
	# 			)
	# 			return list(cur)
	# 	except psycopg2.Error as err:
	# 		error_string = "Get error.\nDetails:" + str(err)
	# 		logging.error(error_string)
	# 	return [{"error": error_string}]
	#
	# def getProductByBand(self, bandName):
	# 	try:
	# 		with DM_PG.__cursor() as cur:
	#
	# 			cur.execute(
	# 				'SELECT * '
	# 				'FROM Product P '
	# 				'WHERE bandName ilike %s', (bandName,)
	# 			)
	# 			return list(cur)
	# 	except psycopg2.Error as err:
	# 		error_string = "Get error.\nDetails:" + str(err)
	# 		logging.error(error_string)
	# 	return [{"error": error_string}]


	def getAllProductsPreferredByUsername(self, username):
		try:
			with DM_PG.__cursor() as cur:
				#--selezionare il genere del prodotto più comprato dall'utente X
				cur.execute(
					'select P.main_genre '
					'from product p '
					'join concerning c on p.id = c.product '
					'join bill b on c.billid = b.id '
					'where b.client = %s '
					'group by p.main_genre '
					'having count(*) >= all ( '
						'select count(*) '
						'from product p '
						'join concerning c on p.id = c.product '
						'join bill b on c.billid = b.id '
						'where b.client = %s '
						'group by p.main_genre) ', (username, username)


				)
				listcur = list(cur)
				preferredGenre = listcur[0]["main_genre"]

				cur.execute(
					'SELECT  * '
					'FROM Product P '
					'LEFT JOIN Band B ON P.bandName = B.bandName '
					'LEFT JOIN Soloist S ON P.soloist = S.stagename '
					'LEFT JOIN Cover C ON C.product = P.id '
					'where P.main_genre = %s',(preferredGenre,)

				)
				return list(cur)

		except psycopg2.Error as err:
			error_string = "Get error.\nDetails:" + str(err)
			logging.error(error_string)
		return [{"error": error_string}]

	'''Method used by buying products. Requires the client to send productID to buy, paymenttype and clientID'''
	def buyProductById(self, productId, clientIP, paymentType, clientUsername):
		currentDate = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
		try:
			with DM_PG.__cursor() as cur:

				cur.execute(
					'INSERT INTO Bill(data,ip_pc,type,client) '
					'VALUES (%s, %s, %s, %s) RETURNING id ', (currentDate, clientIP, paymentType, clientUsername)
				)

				id = cur.fetchone()
				id = id['id']  # {'id':'3'}

				cur.execute(
					'INSERT INTO concerning(billId,Product) '
					'VALUES (%s, %s)', (id, productId)
				)
				# update preferred genre by username
				# cur.execute(
				# 	"UPDATE Client SET favouriteGenre = %s "
				# 	"WHERE username = %s ",(preferredGenre, clientUsername)
				#
				# )
				#ricerco il genere preferito in base agli acquisti degli utenti
				# allPurchasedProducts =  self.getPurchasedProducts(clientUsername)
				# contGenreDict = {"Classica":0, "Rap":0, "Pop":0,"Jazz":0}
				# for genre in allPurchasedProducts:
				# 	print(genre["main_genre"])
				# 	if genre["main_genre"] == "Classica":
				# 		contGenreDict["Classica"] = contGenreDict["Classica"] + 1
				# 	elif genre["main_genre"] == "Rap":
				# 		contGenreDict["Rap"] = contGenreDict["Rap"] + 1
				# 	elif genre["main_genre"] == "Jazz":
				# 		contGenreDict["Jazz"] = contGenreDict["Jazz"] + 1
				# 	else:
				# 		contGenreDict["Pop"] = contGenreDict["Pop"] + 1
				# print(max(contGenreDict, key=contGenreDict.get))
				# preferredGenre = max(contGenreDict, key=contGenreDict.get)


				# #imposto il genere preferito
				# cur.execute(
				# 	"UPDATE Client SET favouriteGenre = %s "
				# 	"WHERE username = %s ",(preferredGenre, clientUsername)
				#
				# )


				return [{"bought": 1}]
		except psycopg2.Error as err:
			error_string = "Buying error.\nDetails:" + str(err)
			logging.error(error_string)
			return [{"error": error_string}]



	'''Return all product bought by the given clientUsername'''
	def getPurchasedProducts(self, clientUsername):
		try:
			with DM_PG.__cursor() as cur:
				cur.execute(
					'SELECT P.id, P.type, P.soloist, P.bandName, B.data, P.main_genre '
					'FROM Product P '
					'JOIN Concerning C ON P.id = C.product '
					'JOIN Bill B ON C.billId = B.id '
					'WHERE B.client = %s ', (clientUsername,)
				)

				return list(cur)
		except psycopg2.Error as err:
			error_string = "Get error.\nDetails:" + str(err)
			logging.error(error_string)
			return [{"error": error_string}]





		# def log(self, idModel: str, instant: datetime, methodName: str):
		#     """Scrive il log sulla tabella InsegnamentiLog che deve \ essere presente nel database cls.__database4Log.
		#     CREATE TABLE INSEGNAMENTILOG (id SERIAL PRIMARY KEY, \ idModeApp VARCHAR NOT NULL , instant TIMESTAMP NOT NULL , \
		#      methodName VARCHAR NOT NULL)"""
		#     if idModel is None or methodName is None or instant is None:
		#         return
		#     with DM_PG.__cursor4log() as cur:
		#         cur.execute("INSERT INTO InsegnamentiLog(idModeApp ,instant , methodName) VALUES (%s,%s,%s)",(idModel , instant , methodName))
		#         if cur.rowcount != 1:
		#             logging.error("Log has not been written. Details: " + idModel + ", " + str(instant) + "," + methodName)
		#             return False
		#         return True

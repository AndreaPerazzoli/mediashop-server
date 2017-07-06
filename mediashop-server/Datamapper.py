import json
from datetime import datetime
import time
import logging
import psycopg2.extras

import getpass

from flask import jsonify


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
					'LEFT JOIN Cover C ON C.product = P.id '
				)

				return list(cur)
		except psycopg2.Error as err:
			error_string = "Get error.\nDetails:" + str(err)
			logging.error(error_string)
			return [{"error": error_string}]


	def searchProductBy(self, attribute, subject):
		attribute = "P." + attribute
		subject = "%" + subject + "%"
		try:
			with DM_PG.__cursor() as cur:
				cur.execute(
					"SELECT * "
					"FROM Product P "
					"LEFT JOIN Cover C ON C.product = P.id "
					"WHERE %s ilike %s ",(attribute, subject)
				)

				return list(cur)
		except psycopg2.Error as err:
			error_string = "Search error.\nDetails:" + str(err)
			logging.error(error_string)
			return [{"error": error_string}]


	def searchProductByPrice(self, minPrice, maxPrice):
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
					'SELECT P.id, P.type, P.soloist, P.bandName, B.data '
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

	#TODO: needs testing
	'''Will return a list of suggested product id if client had a purchase history'''
	def suggestedProducts(self, clientUsername):
		purchased = self.getPurchasedProducts(clientUsername)
		if not purchased:
			return []  # no suggestions
		return self.evaluateSuggestions(purchased)


	'''Wrapper that evaluate suggestions'''
	def evaluateSuggestions(self, purchaseHistory):
		return (self.suggestionsFactoryFrom(self.getProducts(), purchaseHistory)).fetch(20)


	'''Filter product if they are valid suggestions for the client'''
	def suggestionsFactoryFrom(self, allProducts, filter):
		suggestionTips = self.filterForSuggestions(filter)
		suggestions = []
		for row in allProducts:
			if row['id'] not in filter.values and (row['type'] in suggestionTips.values or ((row['soloist']!= None and row['soloist'] in suggestionTips.values) or (row['bandName'] != None and row['bandName'] in suggestionTips['bandName']))):
				suggestions.append(row['id'])
		return suggestions

	'''Filter purchesed protuct to learn some suggestion tips'''
	def filterForSuggestions(self, purchesed):
		# if there aren't recent purchese and this client had bought less than 5 products
		# our suggestions will be based on all his purchese history.
		# Else we will base our suggestion only on recent ones.
		currentDate = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
		aMonth = '01-00 00:00:00'
		suggestionTips = []
		for row in purchesed:
			if (currentDate - row['billData']) > aMonth:
				suggestionTips.append(row)
		if len(suggestionTips) < 5:
			return purchesed
		return suggestionTips

	# def write_blob(self, part_id, path_to_file, file_extension):
	# 	""" insert a BLOB into a table """
	#
	# 	# read data from a picture
	# 	drawing = open(path_to_file, 'rb').read()
	# 	# read database configuration
	#
	#
	# 	# create a new cursor object
	# 	with DM_PG.__cursor() as cur:
	# 		# execute the INSERT statement
	# 		cur.execute("INSERT INTO Cover(product,data_cover,type_cover) " +
	# 		            "VALUES(%s,%s,%s)",
	# 		            (part_id, psycopg2.Binary(drawing), file_extension))
	#
	# def read_blob(self, part_id, path_to_dir):
	# 	""" read BLOB data from a table """
	#
	# 	with DM_PG.__cursor() as cur:
	# 		cur.execute(""" SELECT P.title, C.type_cover, C.data_cover
    #                        FROM Cover C
    #                        INNER JOIN product P on C.product = P.id
    #                        WHERE P.id = %s """, (part_id,))
	#
	# 		blob = cur.fetchone()
	# 		print(blob)
	# 		open(path_to_dir + blob['title'] + '.' + blob['type_cover'], 'wb').write(blob['data_cover'])
		# close the communication with the PostgresQL database





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

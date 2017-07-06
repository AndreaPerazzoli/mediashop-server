
import psycopg2.extras
import logging

class InsertImg:
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
		InsertImg.__open()
		InsertImg.__nIstanze += 1

	def close(self):
		self.__del__()

	def __del__(self):
		InsertImg.__nIstanze -= 1
		InsertImg.__close()
	''' function to populate BD with image'''

	def write_blob(self, part_id, path_to_file, file_extension):
		""" insert a BLOB into a table """

		# read data from a picture
		drawing = open(path_to_file, 'rb').read()
		# read database configuration


		# create a new cursor object
		with InsertImg.__cursor() as cur:
			# execute the INSERT statement
			cur.execute('INSERT INTO Cover(product,data_cover,type_cover) '
						'VALUES(%s,%s,%s) ',
						(part_id, psycopg2.Binary(drawing), file_extension))


	def read_blob(self, part_id, path_to_dir):
		""" read BLOB data from a table """

		with InsertImg.__cursor() as cur:
			cur.execute(
				'SELECT P.title, C.type_cover, C.data_cover '
				'FROM Cover C '
				'INNER JOIN product P on C.product = P.id '
				'WHERE P.id = %s ', (part_id,))

			blob = cur.fetchone()
			print(blob)
			open(path_to_dir + blob['title'] + '.' + blob['type_cover'], 'wb').write(blob['data_cover'])
		# close the communication with the PostgresQL database


if __name__ == '__main__':
	#	dataMapper = DM_PG()
	#	dataMapper.write_blob(1, '/Users/enricogigante/Desktop/mediashop-server/mediashop-server/templates/vasco-rossi-innocente.jpg', 'jpg')
	# dataMapper.read_blob(1,"/Users/enricogigante/Desktop/mediashop-server/mediashop-server/templates/" )
	image = InsertImg()
	#image.write_blob(1, '/Users/enricogigante/Desktop/mediashop-server/mediashop-server/templates/vasco-rossi-innocente.jpg','jpg')
	image.read_blob(1,"/Users/enricogigante/Desktop/mediashop-server/mediashop-server/templates/" )
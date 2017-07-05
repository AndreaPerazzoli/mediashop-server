from Datamapper import DM_PG
import psycopg2


class InsertImg:
	def __init__(self):
		self.datamapper = DM_PG()

	def __del__(self):
		self.datamapper.close()

	''' function to populate BD with image'''

	def write_blob(self, part_id, path_to_file, file_extension):
		""" insert a BLOB into a table """

		# read data from a picture
		drawing = open(path_to_file, 'rb').read()
		# read database configuration


		# create a new cursor object
		with self.datamapper.__cursor() as cur:
			# execute the INSERT statement
			cur.execute('INSERT INTO Cover(product,data_cover,type_cover) '
						'VALUES(%s,%s,%s) ',
						(part_id, psycopg2.Binary(drawing), file_extension))

	def read_blob(self, part_id, path_to_dir):
		""" read BLOB data from a table """

		with self.datamapper.__cursor() as cur:
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
	image.write_blob(1, '/Users/enricogigante/Desktop/mediashop-server/mediashop-server/templates/vasco-rossi-innocente.jpg','jpg')

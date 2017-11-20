import sqlite3, os, threading


def contextmanager(func):
	class ContextManager(object):
		def __init__(self, it):
			self.it = it

		def __enter__(self):
			return self.it.next()

		def __exit__(self, *args):
			try:
				self.it.next()
			except StopIteration:
				pass

	return lambda *args: ContextManager(func(*args))



class DBUpdates(object):
	lock = threading.Lock()

	def __init__(self, connection):
		self.connection = connection


	@contextmanager
	def cursor(self):
		cur = self.connection.cursor()
		yield cur
		cur.close()


	def _create_version_table(self):
		with self.cursor() as cur:
			cur.execute('create table database_version (version INTEGER)')
			cur.execute('insert into database_version (version) values (0)')
			self.connection.commit()

	def _select_version(self):
		with self.cursor() as cur:
			cur.execute('select version from database_version')
			return cur.fetchone()[0]


	def get_version(self):
		try:
			return self._select_version()
		except:
			self._create_version_table()
		return self._select_version()

	def set_version(self, value):
		with self.cursor() as cur:
			cur.execute('update database_version set version=?', [value])
			self.connection.commit()


	def get_update(self, n):
		key = 'update_{0}'.format(n)
		return getattr(self, key, None)


	def check(self):
		with self.lock:
			n = self.get_version() + 1
			while True:
				update = self.get_update(n)
				if not update: break

				update()
				n += 1


	def update_1(self):
		try:
			with self.cursor() as cur:
				cur.execute('select options_string from proadmin_user limit 1')
				cur.fetchone()
				need_update = False
		except:
			need_update = True

		if need_update:
			with self.cursor() as cur:
				cur.execute('alter table proadmin_user add column options_string TEXT;')
				self.connection.commit()

		self.set_version(1)






class DbConnection( object ):
	__local = threading.local()


	def __init__(self, dbfile=None):
		self.dbfile = dbfile or ":memory:"
		self.__db_checked = False


	@property
	def connection(self):
		is_new = (self.dbfile == ":memory:") or (not os.path.exists(self.dbfile))
		if getattr( self.__local, "current_db", None ) is None:
			self.__local.current_db = sqlite3.connect(self.dbfile)
			self.set_busy_timeout()
			if is_new:
				self.recreate()
			else:
				if not self.__db_checked:
					DBUpdates(self.__local.current_db).check()
					self.__db_checked = True

		return self.__local.current_db


	def set_busy_timeout(self):
		cursor = self.connection.cursor()
		cursor.execute('''PRAGMA busy_timeout = 5000;''')
		self.connection.commit()


	def recreate(self):
		cursor = self.connection.cursor();
		cursor.execute('''DROP TABLE IF EXISTS aclobject''')
		cursor.execute('''DROP TABLE IF EXISTS proadmin_user''')
		cursor.execute('''DROP TABLE IF EXISTS proadmin_group''')
		cursor.execute('''DROP TABLE IF EXISTS user_in_group''')
		cursor.execute('''DROP TABLE IF EXISTS rule''')
		self.connection.commit()

		
		cursor = self.connection.cursor();
		cursor.execute('''PRAGMA journal_mode=WAL;''') # WAL corrupting the DB
		cursor.execute('''PRAGMA foreign_keys = ON;''')
		self.connection.commit()


		cursor = self.connection.cursor();

		cursor.execute('''
			CREATE TABLE aclobject (
				guid CHAR(32) PRIMARY KEY,
				object_type CHAR(32),
				parent_guid char(32),
				name TEXT,
				is_dirty INT,
				FOREIGN KEY(parent_guid) REFERENCES aclobject(guid) ON DELETE CASCADE

				)''')

		cursor.execute('''
			CREATE TABLE proadmin_user (
				guid CHAR(32) PRIMARY KEY,
				email VARCHAR(255),
				last_name VARCHAR(255),
				first_name VARCHAR(255),
				password_hash VARCHAR(255),
				phone VARCHAR(255),
				notification_email VARCHAR(255),
				cell_phone VARCHAR(255),
				country VARCHAR(255),
				keywords_string TEXT,
				options_string TEXT
				)''')

		cursor.execute('''
			CREATE TABLE proadmin_group (
				guid CHAR(32) PRIMARY KEY,
				name VARCHAR(255)		
				)''')


		cursor.execute('''
			CREATE TABLE user_in_group (
				user_guid CHAR(32),
				group_guid char(32)
				)''')


		cursor.execute('''
			CREATE TABLE rule (
				subject_guid CHAR(32),
				aclobject_guid CHAR(32),
				access CHAR(1),

				FOREIGN KEY(aclobject_guid) REFERENCES aclobject(guid) ON DELETE CASCADE

				
				)''')
		
		"""
		

		cursor.execute('''
			CREATE INDEX subject_guid_index ON rule (subject_guid);
			''')

		cursor.execute('''
			CREATE INDEX aclobject_guid_index ON rule (aclobject_guid);
			''')

		cursor.execute('''
			CREATE INDEX aclobject_subject_guid_index ON rule (subject_guid, aclobject_guid);
			''')		
		cursor.execute('''
			CREATE INDEX user_guid_index ON user_in_group (user_guid);
			''')
		cursor.execute('''
			CREATE INDEX group_guid_index ON user_in_group (group_guid);
			''')
		"""



		# FOREIGN KEY(group_guid) REFERENCES `group`(`guid`),
		# FOREIGN KEY(aclobject_guid) REFERENCES aclobject(guid),

		self.connection.commit()


	def fetch_one(self, sqlquery, arguments = None):
		#print sqlquery
		if arguments is None:
			arguments = []
		cursor = self.connection.cursor()
		cursor.execute(sqlquery, arguments);
		result = cursor.fetchone()
		cursor.close()
		return result

	def fetch_all(self, sqlquery, arguments = None):
		#print sqlquery
		try:
			if arguments is None:
				arguments = []
			cursor = self.connection.cursor();
			cursor.execute(sqlquery, arguments)
			result = cursor.fetchall()
			cursor.close()
			return result
		except:
			print sqlquery
			raise


	def execute(self, sqlquery, arguments = None):
		#print sqlquery
		if arguments is None:
			arguments = []
		cursor = self.connection.cursor()
		cursor.execute(sqlquery, arguments)
		cursor.close()
		self.connection.commit()


	def executemany(self, sqlquery, arguments = None):
		#print sqlquery
		try:
			if arguments is None:
				arguments = []
			c = self.connection.cursor()

			c.executemany(sqlquery, arguments)
			c.close()
			self.connection.commit()
		except:
			print sqlquery, arguments
			raise



	def build_or_list(self, list_or_dict):
		if isinstance( list_or_dict, list ):
			return " OR ".join( [condition_tuple[0] for condition_tuple in list_or_dict] ), [condition_tuple[1] for condition_tuple in list_or_dict]
		
		if isinstance( list_or_dict, dict ):
			ziped = [("%s IN (%s)"%(k, ",".join(['?']*len(v))), v) for (k, v) in list_or_dict.iteritems() if v]

			return " OR ".join( [condition_tuple[0] for condition_tuple in ziped] ), reduce( lambda a,b: a+b, [condition_tuple[1] for condition_tuple in ziped], [])



	def build_complex_where_clause(self, and_or_condition_value_list):
		"""
		INPUT:
		[ {'some1': [1,2,3], "some2":[1,2,3]},[ ('some1 = ?', 1), ('some2 = ?', 2) ], [('other1 = ?',3), ('other2 = ?', 4)], [('one = ?',5)] ] 
		ANSWERS:
		("(some1 IN (?,?,?)  OR some2 IN (?,?,?)) AND (some1 = ? OR some2 = ?) AND (other1 = ? OR other2 = ?)", [1,2,3,1,2,3,1,2,3,4,5]
		"""
		or_condition_value = [ self.build_or_list(l) for l in and_or_condition_value_list]
		return " AND ". join( [ '(' + or_list[0] + ')' for or_list in or_condition_value if or_list[0] ]  ), reduce(lambda a,b:a+b, [e[1] for e in or_condition_value],[])


	def build_simple_where_clause(self, filter_dict):
		if filter_dict:
			filter_tuples = [ ("%s = ?" % (k,), filter_dict[k]) for k in filter_dict ]
			return " AND ". join([query for (query, value) in filter_tuples]), [value for (query, value) in filter_tuples]
		else:
			return "", []

	def build_where_clause(self, filter_dict_or_list):
		if isinstance(filter_dict_or_list, list): return self.build_complex_where_clause(filter_dict_or_list)
		if isinstance(filter_dict_or_list, dict): return self.build_simple_where_clause(filter_dict_or_list)
		return ""


	def build_update_clause(self, update_dict):
		if update_dict:
			filter_tuples = [ ("%s = ?" % (k,), update_dict[k]) for k in update_dict ]
			return  ", ". join([query for (query, value) in filter_tuples]), [value for (query, value) in filter_tuples]
		else:
			return "", []



	def delete_cmd(self, table_name, filter_dict):
		if filter_dict is None: filter_dict = {}

		where_clause, parameters = self.build_where_clause(filter_dict)
		query = '''DELETE FROM %s %s'''%(table_name, 'WHERE ' + where_clause if where_clause else '')

		return self.execute( query, parameters )

	def update_cmd(self, table_name, update_dict, filter_dict):
		if filter_dict is None: filter_dict = {}
		if update_dict is None: update_dict = {}

		where_clause, where_parameters = self.build_where_clause(filter_dict)
		update_clause, update_parameters = self.build_update_clause(update_dict)
		return self.execute( '''UPDATE %s SET %s %s''' % (table_name, update_clause, 'WHERE ' + where_clause if where_clause else ''), update_parameters + where_parameters)


	def select_cmd(self, table_name, select_list, filter_dict):
		if filter_dict is None: filter_dict = {}

		where_clause, where_parameters = self.build_where_clause(filter_dict)
		select_clause = ', '.join(select_list)
		query = '''SELECT %s FROM %s %s''' % (select_clause, table_name, 'WHERE ' + where_clause if where_clause else '')
		#print query
		return self.fetch_all( query, where_parameters)


	def insert_cmd(self, table_name, select_list, values_list):
		select_clause = ', '.join(select_list)
		values_clause = ', '.join( ["?"] * len(values_list) )
		return self.execute( '''INSERT INTO %s (%s) VALUES (%s)''' % (table_name, select_clause, values_clause), values_list)


	def insertmany_cmd(self, table_name, select_list, values_list):
		if not values_list:
			return
		select_clause = ', '.join(select_list)
		values_clause = ', '.join( ["?"] * len(values_list[0]) )
		return self.executemany( '''INSERT INTO %s (%s) VALUES (%s)''' % (table_name, select_clause, values_clause), values_list)		


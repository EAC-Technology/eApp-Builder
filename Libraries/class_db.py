import threading

class Database( object ):

	#__maindb = None
	__maindb = threading.local()
	__macrosdb = threading.local()

	@classmethod
	def maindb(self):

		application.databases.get_list() # need as a trigger for database init

		if getattr( self.__maindb, "current_db", None ) is None:
			self.__maindb.current_db =  Database(application.databases.dbschema, "dbschema")

		return self.__maindb.current_db

	@classmethod
	def macrosdb(self):

		application.databases.get_list() # need as a trigger for database init
		#if getattr( self.__maindb, "current_db", None ) is None:
		self.__macrosdb.current_db =  Database(application.databases.dbschema_macros, "dbschema_macros")

		return self.__macrosdb.current_db

	@classmethod
	def set_maindb(self,name = ""):

		if name == "dbschema_test":
			self.__maindb.current_db = Database(application.databases.dbschema_test, "dbschema_test")

		return self.__maindb.current_db

	def clean(self):
		if self.name == "dbschema_macros":
			self.commit("""DELETE FROM macros""",)
			self.commit("""DELETE FROM timer""",)
			self.commit("""DELETE FROM plugin""",)
			self.commit("""DELETE FROM custom_event""",)
			self.commit("""DELETE FROM kv_macro_storage""",)
		else:
			self.commit("""DELETE FROM config""",)
			self.commit("""DELETE FROM remote_settings""",)


	def __init__(self, db=None, name = None):
		self.__db = db
		self.name = name

	def fetch_one(self, sqlquery, arguments = None):
		if arguments is None:
			arguments = []

		return self.__db.fetchone(sqlquery, arguments)

	def fetch_all(self, sqlquery, arguments = None):
		if arguments is None:
			arguments = []
		return self.__db.fetchall(sqlquery, arguments)

	def execute(self, sqlquery, arguments = None):
		if arguments is None:
			arguments = []
		return self.__db.execute(sqlquery, arguments)

	def commit(self, sqlquery, arguments = None):
		if arguments is None:
			arguments = []
		self.__db.execute(sqlquery, arguments)
		(lastrowid, count) = self.__db.commit()
		return lastrowid

	def create(self, tablename, arguments=None ):
		if arguments:
			return self.__db.create( tablename, arguments )
		else:
			return self.__db.create( tablename )

	def get_objects_by_name(self):
		return self.__db.get_objects_by_name()

	def get_table(self, id, name):
		return self.__db.get_table( id, name )

	def interrupt( self ):
		return self.__db._VDOM_database__conn.interrupt()


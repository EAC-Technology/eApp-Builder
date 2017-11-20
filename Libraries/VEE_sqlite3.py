from VEE_utils import AutoCast
from VEE_resources import BaseResourceManager, DB_FOLDER
from vscript import generic
from cStringIO import StringIO
import threading, sqlite3, os


#######################################
#Exceptions							  #
#######################################
class DatabaseDoesntExist( Exception ):
	def __init__( self ):
		Exception.__init__( self, 'Database doesn\'t exist' )

class DatabaseUnknownType( Exception ):
	def __init__( self, t ):
		Exception.__init__( self, "Database doesn't support '%s' type" % t.__name__  )

#######################################
#SQLITE DB Wrapper					  #
#######################################
TIMEOUT = 10
class ExternalDatabase( object ):

	local_db_list = threading.local()

	@classmethod
	def open_db( self, name ):

		db = getattr( self.local_db_list, name, None ) is None
		if db is None:
			db = self( name )
			setattr( self.local_db_list,name, db )

		return db

	def __init__(self, dbname ):
		self.conn = sqlite3.connect( dbname , timeout = TIMEOUT )


	def insert(self, query, escapeList=None):
		self.query(query,escapeList)
		# Get the last inserted id
		id = self.query('SELECT last_insert_rowid();')[0][0]
		# Return the id
		return id


	def execute_many( self, query, escapeList ):
		return self.query( query, escapeList, executeMany=True )


	def query(self, query, escapeList=None, executeMany = False ):
		"""
		Perform a query. When an escapeList is provided it'll be used for
		variable substitution.

		Returns a list with dictionaries containing the result of your SELECT,
		or an empty list after an INSERT or UPDATE.
		"""

		# Create a new cursor
		tc = self.conn.cursor()
		tc.execute( "PRAGMA foreign_keys = ON" )
		# Execute our query with or without values to escape
		if( escapeList ):
			if executeMany: tc.executemany( query, tuple(escapeList) )
			else: tc.execute(query, tuple(escapeList))
		else:
			tc.execute(query)

		# Make an empty result list
		result = []
		append = result.append

		# A description is only set after a SELECT statement
		# Even when there are no results.
		if(tc.description):
			# Fetch the field names out of our cursor
			#field_names = [d[0].lower() for d in tc.description]

			# Generate a dictionary
			while True:
				rows = tc.fetchmany()
				if not rows: break
				for row in rows: append(row)
	   	else:
			# If there is no description this must mean we're doing an insert
			# or update. Anything that needs a commit.
			self.conn.commit()

		# Close the cursor
		tc.close()

		# Return the list with the dictionaries
		return result


	def truncate(self, tablename):
		"""
		Delete all rows from a table and reset the autoincrement
		"""

		# Create a new cursor
		tc = self.conn.cursor()

		# Clear the table
		tc.execute("delete from "+ tablename + ";")
		# Reset the autoincrement
		#tc.execute("delete from sqlite_sequence where name='"+ tablename + "';")
		tc.close()


	def force_close( self ):

		self.conn.interrupt()
		self.conn.close()


	def save_close( self ):

		self.conn.commit()
		self.force_close()


	def unlock_db( self ):
		self.conn.interrupt()



#######################################
#DB Manager Class		  			  #
#######################################

class DatabaseManager( BaseResourceManager ):
	"""Class for manage DB Sqlite files.
		All db files are stored in ./db folder
	"""

	def __init__( self, plugin_guid ):
		BaseResourceManager.__init__( self, plugin_guid )
		self._path = DB_FOLDER

	databaselist 	= property( lambda x: x.listdir( "." ) )
	import_db 		= BaseResourceManager.write
	export_db		= BaseResourceManager.open
	delete_db		= BaseResourceManager.delete


	def open_db( self, name ):
		if self.exists( name ): return ExternalDatabase( os.path.join( self.abs_path(), name ) )
		else: raise DatabaseDoesntExist

	def create_db( self, name ):
		if not self.exists( name ):
			self.import_db( name, StringIO() )



#######################################
#VScript wrappers					  #
#######################################
class v_ExternalDatabase( generic ):

	def __init__( self,  db ):
		self.db = db


	@AutoCast
	def v_insert(self, query, escapeList = None ):
		return self.db.insert( query, escapeList )


	@AutoCast
	def v_query(self, query, escapeList=None, executeMany = False  ):
		return self.db.query( query, escapeList, executeMany )


	def v_executemany( self, query, escapeList ):
		return self.v_query( query, escapeList, True )



class v_DatabaseManager( generic ):

	def __init__( self, plugin_guid ):
		self.db_manager = DatabaseManager( plugin_guid )
		self.data_bases = {}


	@AutoCast
	def __call__( self, name ):

		db = self.data_bases.get( name, None )
		if not db:
			try:
				db = self.db_manager.open_db( name )
			except DatabaseDoesntExist, ex:
				self.db_manager.create_db( name )
				db = self.db_manager.open_db( name )

			self.data_bases[ name ] = db

		return v_ExternalDatabase( db )


	@AutoCast
	def v_exists( self, name ):
		return self.db_manager.exists( name )

	@AutoCast
	def v_deletedatabase( self, name ):
		self.db_manager.delete( name )

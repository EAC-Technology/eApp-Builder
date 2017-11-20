from VEE_std_lib import v_buffer, v_BaseException
from VEE_utils import AutoCast
from vscript import generic
import os, urllib


def fullpath( fn ):
	def wrapper( *args, **kwargs ):
		arguments = list( args )
		self, path = arguments[:2]
		arguments[1] = os.path.join( self.plugin_path(), os.path.basename( path ) )
		return fn( *arguments, **kwargs )
	return wrapper



TMP_FOLDER = "tmp"
RES_FOLDER = "res"
DB_FOLDER = "db"



class v_res_file( v_buffer ):

	def __init__( self, path, mode="rb", file_obj = None ):
		v_buffer.__init__( self, "" )
		self.mode = "rb"
		self.path = application.storage.abs_path( path )


	def open( self ):
		return application.storage.open( self.path, self.mode )



class StorageManager( object ):

	@classmethod
	def open( self, path, mode = "rb" ):
		if self.exists( path ): return application.storage.open( path, mode )
		else: raise Exception( "Open: no such path: %s" % path )


	@classmethod
	def delete( self, path ):
		if self.exists( path ): return application.storage.delete( path )
		else: raise Exception( "Delete: no such path: %s" % path )


	@classmethod
	def write( self, path, fd ):
		return application.storage.write( path, fd )


	@classmethod
	def getsize( self, path ):
		if self.exists( path ): return application.storage.getsize( path )
		else: raise Exception( "GetSize: no such path: %s" % path )


	@classmethod
	def mkdir( self, path ):
		if not self.exists( path ): application.storage.mkdir( path )
		else: raise Exception( "mkdir: such path already exist: %s" % path )


	@classmethod
	def exists( self, path ):
		return application.storage.exists( path )


	@classmethod
	def isfile( self, path ):
		return application.storage.isfile( path )


	@classmethod
	def isdir( self, path ):
		return application.storage.isdir( path )


	@classmethod
	def listdir( self, path ):
		return application.storage.listdir( path )



_PUBLIC_URL = "/get_plugin_resource?guid={0}&name={1}&type={2}"



class BaseResourceManager( object ):

	def __init__( self, plugin_guid ):
		self._plugin_guid = plugin_guid
		self._path = ""


	plugin_guid	 = property( lambda x: x._plugin_guid )
	path		 = property( lambda x: x._path )


	@fullpath
	def open( self, path, mode="rb" ):
		return StorageManager.open( path, mode )


	@fullpath
	def delete( self, path ):
		StorageManager.delete( path )


	@fullpath
	def write( self, path, fd ):
		StorageManager.write( path, fd )


	@fullpath
	def size( self, path ):
		return StorageManager.getsize( path )


	def mkdir( self, path ):
		pass


	@fullpath
	def exists( self, path ):
		return self._exists( path )


	def _exists( self, path ):
		return StorageManager.exists( path )


	@fullpath
	def isfile( self, path ):
		return StorageManager.isfile( path )


	@fullpath
	def isdir( self, path ):
		return StorageManager.isdir( path )


	@fullpath
	def listdir( self, path ):
		return StorageManager.listdir( path )


	def plugin_path( self ):
		return 	os.path.join( self.plugin_guid, self.path ) \
				if self._path else self.plugin_guid


	def abs_path( self ):
		return application.storage.abs_path( self.plugin_path() )


	def delete_all( self ):
		for res in self.listdir( "." ): self.delete( res )


	def public_link( self, name, res_type ):
		return _PUBLIC_URL.format(
						self.plugin_guid,
						urllib.quote( name ),
						res_type	)



class ResourceManager( BaseResourceManager ):
	"""Class for manage resources.
		All resources are stored in ./res folders
	"""

	def __init__( self, plugin_guid, path ):
		BaseResourceManager.__init__( self, plugin_guid )
		self._path = path


	def abs_path( self, file_name ):
		return os.path.join( BaseResourceManager.abs_path( self ), os.path.basename( file_name ) )

	def public_link( self, name ):
		return super( ResourceManager, self ).public_link( name, self._path )


	resourcelist	= property( lambda x: x.listdir( "." ) )
	import_res 		= BaseResourceManager.write
	export_res		= BaseResourceManager.open
	delete_res		= BaseResourceManager.delete



ResourceFolderManager = lambda guid: ResourceManager( guid, RES_FOLDER )
TemporaryFolderManager = lambda guid: ResourceManager( guid, TMP_FOLDER )



def create_plugin_dir( guid ):
	if not StorageManager.exists( guid ):
		StorageManager.mkdir( guid )
		for p in [ TMP_FOLDER, RES_FOLDER, DB_FOLDER ]:
			StorageManager.mkdir( os.path.join( guid, p ) )



def delete_plugin_dir( guid ):
	if StorageManager.exists( guid ): application.storage.rmtree( guid )



class v_BaseResourceManager( generic ):

	def __init__( self ):
		self.manager = None


	@AutoCast
	def v_resources( self ):
		return self.manager.resourcelist


	@AutoCast
	def v_size( self, name ):
		return self.manager.size( name )


	@AutoCast
	def v_exists( self, name ):
		return self.manager.exists( name )


	@AutoCast
	def v_open( self, name, mode="rb" ):
		return v_res_file( self.manager.abs_path( name ), mode )


	@AutoCast
	def v_write( self, name, fd ):
		self.manager.write( name, fd.handler )


	@AutoCast
	def v_delete( self, name ):
		self.manager.delete( name )


	@AutoCast
	def v_publiclink( self, name ):
		return self.manager.public_link( name )


	def v_delete_all( self ):
		self.manager.delete_all()


	#Obsolete namse
	v_public_link = v_publiclink



class v_ResManager( v_BaseResourceManager ):

	def __init__( self, plugin_guid ):
		v_BaseResourceManager.__init__( self )
		self.manager = ResourceFolderManager( plugin_guid )


	@AutoCast
	def v_open( self, name ):
		return v_BaseResourceManager.v_open( self, name, "rb" )


	@AutoCast
	def v_write( self, name, fd ):
		raise Exception( "This method doesn't support")


	@AutoCast
	def v_delete( self, name ):
		raise Exception( "This method doesn't support")



class v_TempResManager( v_BaseResourceManager ):

	def __init__( self, plugin_guid ):
		v_BaseResourceManager.__init__( self )
		self.manager = TemporaryFolderManager( plugin_guid )




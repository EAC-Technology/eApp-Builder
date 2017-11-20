import managers
import json
def is_admin():
	# get server's user
	user = managers.request_manager.current.session().user
	return user == u'root'

#response changed form xml to json 10.01.2013 Nikita

def success_result():
	send_response( json.dumps( ["success"] ) )


def error_result( message = '' ):
	send_response( json.dumps( ['error', message] ) )


def send_response( message ):
	session[ 'response' ] = message



class PermissionDeniedError( Exception ):
	pass


try:
	if not is_admin():
		raise PermissionDeniedError()

	import json
	from xml.dom.minidom import parseString
	from class_macro import Macros
	from class_plugins import Plugins
	from class_timer import Timer
	from class_custom_event import CustomEvent
	from class_xml_macro import XMLMacros
	from class_xml_timer import XMLTimer
	from class_xml_plugin import XMLPlugin
	from class_xml_plugin_db import XMLPluginDB
	from class_xml_resource import XMLResource
	from class_xml_custom_event import XMLCustomEvent
	from utils.uuid import uuid4
	import base64
	from VEE_resources import create_plugin_dir, ResourceFolderManager
	from VEE_sqlite3 import DatabaseManager

	xml_data = request.arguments.get('xml_data', None)
	plugin_xml = base64.b64decode(xml_data)
	try:
		dom = parseString( plugin_xml)
		node = XMLPlugin( dom )

		plugin = Plugins()

		plugin.name = node.name
		plugin.description = node.description
		plugin.guid = node.guid
		plugin.version = node.version
		plugin.author = node.author

		exist_plugin = Plugins.get_by_guid(plugin.guid)
		if exist_plugin:
			if exist_plugin.version > plugin.version:
				raise Exception("You can't install old version plugin")
			else:
				if exist_plugin.picture:
					application.storage.delete( exist_plugin.picture )
				exist_plugin.delete()

		plugin.picture = ""
		if node.picture:
			plugin.picture = str(uuid4())
			application.storage.write( plugin.picture, base64.b64decode(node.picture))

		plugin.save()

		create_plugin_dir( plugin.guid )
		dbManager = DatabaseManager( plugin.guid )
		resManager = ResourceFolderManager( plugin.guid )

		for child in node.childs:

			if child.tag == "timer":
				child = XMLTimer( child )
				if child.name:
					timer = Timer()
					timer.fill_from_xml( child, node.guid )

			elif child.tag == "custom_event":
				child = XMLCustomEvent( child )
				if child.name:
					custom_event = CustomEvent()
					custom_event.fill_from_xml( child, node.guid )

			elif child.tag == "macro":
				child = XMLMacros( child )
				if child.name and child.source:
					macros = Macros()
					macros.fill_from_xml( child, node.guid )

			elif child.tag == "database":
				child = XMLPluginDB( child )
				if child.name:
					dbManager.import_db( child.name, base64.b64decode( child.db_source ) )

			elif child.tag == "resource":
				child = XMLResource( child )
				if child.name:
					resManager.import_res( child.name, base64.b64decode( child.res_source ) )


	except Exception, ex:
		raise Exception(ex)

	success_result()

except PermissionDeniedError:
	error_result( 'Permission denied' )

except Exception as ex:
	error_result( ex.message )

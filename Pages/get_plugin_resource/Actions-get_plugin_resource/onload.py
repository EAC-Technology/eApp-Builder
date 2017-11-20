from VEE_resources import ResourceFolderManager, TemporaryFolderManager
import localization

lang = localization.get_lang()
try:
	plugin_guid = request.arguments[ "guid" ]
	name = request.arguments[ "name" ]
	type = request.arguments[ "type" ]

	res_manager = ResourceFolderManager if type == "res" else TemporaryFolderManager
	res_manager = res_manager( plugin_guid )
	if res_manager.exists( name ):
		response.send_file( name, res_manager.size( name ), res_manager.open( name ) )
	else:
		response.terminate()
except Exception, ex:
	self.growl.title = lang["error"]
	self.growl.text = lang["unknown_error"]
	self.growl.active = "1"

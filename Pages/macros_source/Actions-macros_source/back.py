from class_macro import Macros
from class_plugins import Plugins

macro_id = request.shared_variables["macro_id"]
macro = Macros.get_by_id(macro_id)
plugin = Plugins.get_by_guid(macro.plugin_guid)
self.action( "goTo", "/plugin_details?id={0}".format(plugin.id) if plugin else "/plugins" )

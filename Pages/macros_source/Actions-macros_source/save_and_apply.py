from class_macro import Macros
from class_plugins import Plugins


def check():
	from VEE_tools import compile, VScriptComlipationError, PythonCompilationError
	try:
		compile( source )
		return "Passed well."
		self.growl.action( 'show', ["Message", u"No errors in code."] )
	except VScriptComlipationError as error:
		return u"VScript Compilation Error (Line {line}): {msg}".format(
						line = error.line,
						msg	 = error.message )
	except PythonCompilationError as error:
		return u"Python Compilation Error: {msg}".format( msg = error.message )

macro_id = request.shared_variables["macro_id"]
macro = Macros.get_by_id(macro_id)
plugin = Plugins.get_by_guid(macro.plugin_guid)
if plugin and macro:
	source = self.form_macros.codeeditor_macros_body.value = request.arguments.get("codeeditor_macros_body", "")
	macro.code = source
	macro.save()
	result = check()
	self.growl.action( 'show', ["Message", u"Your work is saved! Compilnig: {0}".format( result )] )


else:
	self.growl.action( 'show', ["Error =(", u"Can't save code macro. Please, try to reload the page."] )

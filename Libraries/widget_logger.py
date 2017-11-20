from functools import partial
from VEE_core import engine
from VEE_logs import PluginMessage, PluginMessageError, EngineMessage
from cgi import escape


class WidgetLogsFilter( object ):

	@classmethod
	def plugins_dict( self ):
		from class_plugins import Plugins
		import localization, collections

		lang = localization.get_lang()

		data = collections.OrderedDict()
		data["all"] = lang.get( "log_all_messages", "All messages" )

		for plugin in Plugins.get_all():
			data[ "p" + plugin.guid ] = plugin.name
			for macros in plugin.get_macros():
				data[ "m" + macros.guid ] = "--" + macros.name

		return data


	@classmethod
	def render( self, 	pluginDropDown,
						startDate, startHour, startMinute,
						endDate, endHour, endMinute ):

		from class_plugins import Plugins
		from datetime import datetime
		import json

		pluginDropDown.value = json.dumps( self.plugins_dict() )


		startHour.value = startHour.value1 = endHour.value = endHour.value1 =  \
								"|".join( map( str, xrange( 0, 24 ) ) )

		startMinute.value = startMinute.value1 = endMinute.value = endMinute.value1 =  \
								"|".join( map( str, xrange( 0, 60 ) ) )

		startHour.selectedvalue = endHour.selectedvalue = "12"
		startMinute.selectedvalue = endMinute.selectedvalue = "30"

		startDate.value = endDate.value = datetime.now().strftime( "%Y-%m-%d" )



date_format = "%d.%m.%Y %H:%M:%S"
row_template = u"<tr><td>{date}</td><td>{data}</td></tr>"


class WidgetLogs( object ):

	def __init__( self, filter = None ):
		self.filter = filter


	def render( self, htmlcontaier, action = False ):

		js_script = u"""<script type="text/javascript">
		jQuery( document ).ready( function()
		{{ jQuery("div#o_{id}").scrollTop(999999); }} );
		</script>""".format( id = htmlcontaier.id.replace("-","_") )

		html = u"""<style>table#logstable td{{ word-break: break-all;}}</style>
					<table id="logstable" with="860px">
						<tr>
							<td width="150px"></td><td width="710px"></td>
						</tr>{0}
					</table>"""

		data = []

		if not self.filter:
			data = map( self.format_log_msg, engine.engine_logger )
		else:
			data = [ self.format_log_msg( log ) for log in engine.engine_logger \
											if self.filter( log ) ]

		html = js_script + html.format( "".join( data ) )

		if action:
			htmlcontaier.action( "setHTML", [ html ] )
		else:
			htmlcontaier.htmlcode = html


	def format_log_msg( self, msg  ):
		func = None
		if isinstance( msg, EngineMessage ):
			func = self.format_engine_message
		elif isinstance( msg, PluginMessageError ):
			func = self.format_plugin_error
		else:
			func = self.format_engine_message

		return  row_template.format( 	date = msg.date.strftime( date_format ),
										data = func( msg ) )


	def format_engine_message( self, msg ):
		return  escape( msg.displayed_message() )



	def format_plugin_error( self, msg ):
		return u"""<font color="red">{0}</font>""".format( escape( msg.displayed_message().replace( "<", "&lt;" ) ) )


	@classmethod
	def clear_log( self ):
		engine.clear_log()




def filter( msg, macros_guid = None, plugin_guid = None, start = None, end = None ):
	if not isinstance( msg, PluginMessage ):
		return False

	if not (start or end ) and ( macros_guid or plugin_guid ):
		return msg.macros_guid == macros_guid or msg.plugin_guid == plugin_guid
	elif (start or end ) and ( macros_guid or plugin_guid):
		return ( start <= msg.date and msg.date <= end ) and ( msg.macros_guid == macros_guid or msg.plugin_guid == plugin_guid )
	else:
		return start <= msg.date and msg.date <= end


def create_log_filter( macros_guid = None, plugin_guid = None, start = None, end = None  ):
	return partial( filter, macros_guid = macros_guid, plugin_guid = plugin_guid, start = start, end = end)




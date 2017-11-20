from models import AppScript
from cgi import escape

#########
import urllib
import json
from base64 import b64decode, b64encode, urlsafe_b64decode

from appinmail_sso_client import AppinmailClient
from appinmail_sso_utils import Utils

import ProAdmin
from promail_eac import EACContent
from promail_eac_helper import eacviewer_authenticated, process_vdomxml_resources


def process_wholexml(wholexml):
    eac = EACContent(wholexml)  # EACContent(decode_wholexml(wholexml))
    wholedata = eac.wholedata
    login = wholedata['api']['methods'].get('login', None)
    get = wholedata['api']['methods'].get('get', None)
    post = wholedata['api']['methods'].get('post', None)
    pattern = get.get('pattern', '') if get else ''
    if pattern:
        pattern = json.dumps(pattern)
    pattern_post = post.get('pattern', '') if post else ''
    if pattern_post:
        pattern_post = json.dumps(pattern_post)
    return {
        'session_token': wholedata['global'].get('SessionToken', ''),
        'login_container': login['container'] if login else '',
        'login_action': login['action'] if login else '',
        'get_container': get['container'] if get else '',
        'get_action': get['action'] if get else '',
        'pattern': pattern,
        'post_container': post['container'] if post else '',
        'post_action': post['action'] if post else '',
        'pattern_post': pattern_post,
        'app_id': wholedata['api']['appID'],
        'server': wholedata['api']['server'],
        'vdomxml': wholedata['vdom'],
        'events': wholedata['events'],
        'static': '1' if eac.is_static() else ''
    }


#########



script_id = request.arguments.get('script_id', '')
command = request.arguments.get('command', 'update')

app_script = AppScript.get(guid=script_id)

if app_script:
	if command == 'wholexml':

		input_params = {
			'eac_token': True,
			'session_token': False,
			'login_container': False,
			'login_action': False,
			'get_container': False,
			'get_action': False,
			'post_container': False,
			'post_action': False,
			'app_id': False,
			'server': False,
			'attachments': False,
			'pattern': False,
			'pattern_post': False,
			'email': True,
			'vdomxml': False,
			'events': False,
			'static': False,
		}

		# parameters to apply base64 encoding
		enc = ['pattern', 'pattern_post']
		# parameters that won't be saved in shared variables
		skip = ['vdomxml', 'events', 'static']

		params = {}

		wholexml = app_script.source
		if wholexml:
			params = process_wholexml(wholexml)

		for arg in input_params:
			value = request.arguments.get(arg, None)
			if value is not None or arg not in params:
				params[arg] = value
			if not params[arg] and input_params[arg]:
				raise ValueError(arg)

		for arg in params:
			if arg in skip:
				continue
			if params[arg] and arg in enc:
				response.shared_variables[arg] = b64encode(params[arg])
			else:
				response.shared_variables[arg] = params[arg]

		if params['static'] and params['static'] != '0':
			self.eactimer.active = "0"
		else:
			self.eactimer.active = "1"
		if params['vdomxml']:
			self.dialog_preview.eacviewer.vdomxml = process_vdomxml_resources(
				vdomxml=params['vdomxml'],
				server=params['server'])
			if params['events']:
				self.dialog_preview.eacviewer.vdomactions = params['events']


########
#		self.dialog_preview.hypertext1.htmlcode = escape(str(params))
		self.dialog_preview.show = '1'

	elif command == 'play':
		from VEE_tools import 	compile, execute, PythonCompilationError, VScriptComlipationError,\
						PythonExecutionError, VScriptExecutionError, StopExecutionError, \
						VScriptInternalError
		from VEE_vmacro_dispatcher import STD_ENV_DICT

		compiled_code, debug_info = compile(app_script.source, dict(STD_ENV_DICT))

		try:
			execute( compiled_code, debug_info)

		except VScriptInternalError as error:
			report = u"\n{}".format(error.report) if getattr(error, "report", None) else ""
			raise Exception(unicode(error) + report)

		except VScriptExecutionError as error:
			raise Exception("VScript Execution Error")

		except StopExecutionError as error:
			pass
		except PythonExecutionError as error:
			try:
				from utils.tracing import format_exception_trace
				raise Exception(u"Python Execution Error: " + format_exception_trace(locals=True))
			except ImportError:
				from vdom_trace import Trace
				msg = [ u"Python Execution Error:" ]
				msg.extend( Trace.print_traceback() )
				msg.append( u"Exception: {0}".format( error.message ) )
				raise Exception( u" --> ".join( msg ) )

		self.growl.action("show", ["Launched", "Script successfully launched" ] )

	else:

		disabled = '2' if command == 'delete' else '0'

		form = self.dialog_update.form_update

		form.tab_script_detail.tab_params.input_title.value = app_script.name
		form.tab_script_detail.tab_params.input_title.mode = disabled
		form.tab_script_detail.tab_params.application_id.value = app_script.application_id
		form.tab_script_detail.tab_params.script_id.value = app_script.guid
		form.tab_script_detail.tab_params.command.value = command

		form.tab_script_detail.tab_source.input_source.value = escape(app_script.source or "")
		form.tab_script_detail.tab_source.input_source.mode = disabled

		self.dialog_update.form_update.btn_update.label = command.title()
		self.dialog_update.form_update.tab_script_detail.tab_params.error_name.value = ''
		form.btn_update.action( "setClass", [ 'btn btn-danger' if command == 'delete' else 'btn btn-success' ] )
		self.dialog_update.title = 'Script {}'.format(command.title())
		self.dialog_update.show = '1'

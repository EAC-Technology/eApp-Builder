from utils.uuid import uuid4


def safe_str(input_str, maxlen=30, text_only=False, hint=""):
	TEMPLATE = u"""
		<a title='%(orig)s'>%(short)s<a>
	"""
	short_str = input_str if len(input_str) < maxlen else u"%s..."%input_str[:maxlen]
	if text_only:
		result = short_str
	else:
		result = TEMPLATE % {
			"orig" : input_str if not hint else hint,
			"short" : short_str
		}

	return result

def limit_length( input_str, length_limit ):
	return input_str if len( input_str ) < length_limit else "%s..."%input_str[:length_limit]

def session_put( key, value ):
	if value:
		session_key = request.shared_variables[ key ]
		if not session_key:
			session_key = str( uuid4() )
		session[ session_key ] = value
		response.shared_variables[ key ] = session_key
	else:
		session_key = request.shared_variables[ key ]
		if session.get( session_key ):
			del session[ session_key ]
		del response.shared_variables[ key ]


def session_get( key ):
	return session.get( request.shared_variables[ key ] )


def current_page_name():
	from managers import request_manager
	env = request_manager.get_request().environment().environment()
	#raise Exception(str(env)) # to look through env on appropriate params
	result = env["SCRIPT_NAME"] if "SCRIPT_NAME" in env else "/home.vdom"
	result = result.split("/")[1].split(".")[0]

	return result

def get_env_argument(key):
	from managers import request_manager
	env = request_manager.get_request().environment().environment()
	result = env[key] if key in env else ""
	return result

def get_logout_back_url():
	result = get_env_argument("REQUEST_URI").replace('&',"%26")
	return result

def convert_bytes( bytes ):
	bytes = float( bytes )
	if bytes >= 1099511627776:
		terabytes = bytes / 1099511627776
		size = '%.2fTb' % terabytes
	elif bytes >= 1073741824:
		gigabytes = bytes / 1073741824
		size = '%.2fGb' % gigabytes
	elif bytes >= 1048576:
		megabytes = bytes / 1048576
		size = '%.2fMb' % megabytes
	elif bytes >= 1024:
		kilobytes = bytes / 1024
		size = '%.2fKb' % kilobytes
	else:
		size = '%.2fb' % bytes
	return size

import json
import urlparse
from urllib import urlencode
from base64 import b64decode

import resource_cache

EACVIEWER = 'eacviewer'

import ProAdmin

def eacviewer_authenticated(method):
    def wrapper(*args, **kwargs):
        user = ProAdmin.current_user()
        if not user:
            try:
                back_url = '?'.join([
                    urlparse.urlsplit(request.environment.get('REQUEST_URI', '')).path,
                    request.environment.get('QUERY_STRING', '')
                ])
            except Exception as ex:
                debug(str(ex))
                raise
            params = {'back_url': back_url}
            user_login = request.arguments.get('email', None)
            if user_login:
                params['user_login'] = user_login
            params = urlencode(params)
            response.redirect('/login?' + params)
        else:
            return method()
    return wrapper

def read_attachments():
    # format: name1,id1|name2,id2|...
    sv_keys = request.shared_variables.keys()
    attachments = request.shared_variables['attachments'] \
                  if 'attachments' in sv_keys else []
    if attachments:
        try:
            attachments = [x.split(",", 1) for x in attachments.split("|")]
            for x in attachments:
                if len(x) != 2:
                    raise ValueError()
        except:
            raise ValueError('attachments')
    return attachments

def read_pattern(name='pattern'):
    sv_keys = request.shared_variables.keys()
    pattern = request.shared_variables[name] \
              if name in sv_keys else []
    if pattern:
        try:
            pattern = b64decode(pattern)
            pattern = json.loads(pattern)
        except:
            if pattern == "{}":
                pattern = {}
            else:
                raise ValueError(name)
    return pattern

def read_params():
    # True/False whether parameter is required
    input_params = {
        'eac_token': True,
        'session_token': False,
        'login_container': False,
        'login_action': False,
        'get_container': False,
        'get_action': False,
        'post_container': False,
        'post_action': False,
        'app_id': True,
        'server': True,
    }
    params = {}
    sv_keys = request.shared_variables.keys()
    for arg in input_params:
        params[arg] = request.shared_variables[arg] if arg in sv_keys else ""
        if not params[arg] and input_params[arg]:
            raise ValueError(arg)
    return params

def process_vdomxml_resources(eac=None, vdomxml=None, server=None):
    if eac is not None:
        p = eac.original_server.split('://')
        vdomxml = eac.wholedata['vdom']
    else:
        p = server.split('://')

    return resource_cache.replace_all_resource_links(vdomxml,
                                        p[-1], p[0] if len(p) > 1 else "http")

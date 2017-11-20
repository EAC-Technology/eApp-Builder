"""
"""

import json
import md5
import urlparse
import urllib
import urllib2
import email
import email.utils

from xml.dom.minidom import parseString
from xml.dom import getDOMImplementation

import ProAdmin
from prosuite_logging import app_logger
from prosuite_utils import CachedProperty
from prosuite_rest_api import VDOMRestSession, VDOMRestSessionClosed
from vdom_xml_node import append_cdata
from prosuite_utils import ensure_https
from prosuite_localization_utils import get_lang

logger = app_logger.getChild("EAC")

def getText(nodelist):
    rc = []
    for node in nodelist:
        if isData(node):
            rc.append(node.data)
    return ''.join(rc)

def isData(node):
    return node.nodeType in (node.TEXT_NODE, node.CDATA_SECTION_NODE)


class EACContent(object):

    class EACParseException(Exception):
        pass

    class CantParseRawWholeXMLError(EACParseException):
        pass

    class InvalidWholeXMLError(EACParseException):
        pass

    class InvalidAPIMethodPattern(EACParseException):
        pass

    class InvalidEventsDefinition(EACParseException):
        pass


    def __init__(self, wholexml):
        self.wholedata = self.parse_wholexml(wholexml)

    def _parse_api_section(self, api):
        """
        """
        result = dict(api.attributes.items())
        result['methods'] = {}

        for child in api.childNodes:
            if isData(child):
                continue

            name = child.tagName.lower()
            result['methods'][name] = dict(child.attributes.items())
            result['methods'][name]['pattern'] = ""

            pattern_el = child.getElementsByTagName("PATTERN")
            if not pattern_el:
                continue

            pattern = getText(pattern_el[0].childNodes).strip()
            if pattern:
                try:
                    pattern = json.loads(pattern)
                except:
                    if pattern == "{}":
                        pattern = {}
                    else:
                        raise self.InvalidAPIMethodPattern

            result['methods'][name]['pattern'] = pattern

        return result

    def _parse_item(self, item):
        result = {
            'plugin': '',
            'vdom': ''
        }
        vdomxml_el = item.getElementsByTagName("VDOMXML")
        if vdomxml_el:
            result['vdom'] = getText(vdomxml_el[0].childNodes)#.replace("]]", "]]")
        plugin_el = item.getElementsByTagName("PLUGIN")
        if plugin_el:
            result['plugin'] = plugin_el[0].attributes.get("id", "")
        return result

    def _parse_tags(self, tags):
        result = []
        for child in tags.childNodes:
            if isData(child):
                continue
            if child.tagName.lower() == "tag":
                result.append(dict(child.attributes.items()))
        return result

    def _parse_metadata_section(self, metadata):
        result = {
            'tags': '',
            'item': ''
        }
        tags_el = metadata.getElementsByTagName("TAGS")
        if tags_el:
            result['tags'] = self._parse_tags(tags_el[0])
        item_el = metadata.getElementsByTagName("ITEM")
        if item_el:
            result['item'] = self._parse_item(item_el[0])
        return result

    def parse_wholexml(self, wholexml):

        try:
            dom = parseString(wholexml)
        except Exception:
            raise
            raise self.CantParseRawWholeXMLError

        result_whole = {
            'global': '',
            'api': '',
            'events': '',
            'vdom': '',
            'metadata': {}
        }

        whole_el = dom.getElementsByTagName("WHOLEXML")

        if whole_el and whole_el[0].tagName.lower() != "wholexml":
            raise self.InvalidWholeXMLError

        whole_el = whole_el[0]
        result_whole['global'] = dict(whole_el.attributes.items())

        api_el = whole_el.getElementsByTagName("API")
        if api_el:
            result_whole['api'] = self._parse_api_section(api_el[0])

        events_el = whole_el.getElementsByTagName("EVENTS")
        if events_el:
            result_whole['events'] = getText(events_el[0].childNodes)

        vdomxml_el = whole_el.getElementsByTagName("VDOMXML")
        if vdomxml_el:
            result_whole['vdom'] = getText(vdomxml_el[0].childNodes).replace("]]", "]]")

        metadata_el = whole_el.getElementsByTagName("METADATA")
        if metadata_el:
            result_whole['metadata'] = self._parse_metadata_section(metadata_el[0])

        return result_whole

    def is_static(self):
        return self.wholedata['global']['Content'].lower() == 'static'

    def is_external(self):
        return self.wholedata['global']['Auth'].lower() == 'external'

    def is_internal(self):
        return self.wholedata['global']['Auth'].lower() == 'internal'


EAC_SESSION_TOKEN_KEY = "EAC_SESSION_TOKEN"


def get_server_name(server):
    s = server.split("://", 1)[-1]
    parts = s.rsplit(":", 1)
    s = parts[0]
    if len(parts) == 2:
        port = parts[1]
        s = s.replace("-" + port, "")
    return s


def session_token_key(server, app, eac_token):
    return "".join([get_server_name(server), app, eac_token])


def save_session_token(server, app, eac_token, session_token):
    t = session.get(EAC_SESSION_TOKEN_KEY, None)
    if t is None:
        session[EAC_SESSION_TOKEN_KEY] = {}
        t = session[EAC_SESSION_TOKEN_KEY]
    t[session_token_key(server, app, eac_token)] = session_token


def get_session_token(server, app, eac_token):
    t = session.get(EAC_SESSION_TOKEN_KEY, None)
    if t is None:
        return None
    return t.get(session_token_key(server, app, eac_token), None)


class BaseEACConnector(object):

    def __init__(self, server, app_id, eac_token, session_token,
                 caller='promail', auth='internal'):
                     #TODO: auth should not have default value
        self.server = server
        self.original_server = server
        self.app_id = app_id
        self.eac_token = eac_token
        self.session_token = get_session_token(self.server, self.app_id,
                                               self.eac_token)
        if self.session_token is None:
            self.session_token = session_token
        self.caller = caller
        self.auth = auth


    @property
    def remote_login_info(self):
        return session.get('eac_remote_login_info', {}) or {}

    @remote_login_info.setter
    def remote_login_info(self, value):
        session['eac_remote_login_info'] = value


    def local(self):
        return self.__is_local(self.server)

    def __is_local(self, server):
        s = server.split('://', 1)[-1].split(':', 1)[0]
        return (str(s.lower()) in ['localhost', '127.0.0.1'])

    def __is_cloud(self, server):
        s = server.split('://')[-1].split(':')[0]
        return (s.startswith(ProMail.promail_cloud_host_start) \
            and s.endswith(ProMail.promail_domain()))

    def __is_https(self, server):
        return server.lower().startswith('https://')

    def __is_internal_auth(self):
        return (self.auth.lower() == 'internal')

    def get_certdata(self):
        return self.vdom_connector.get_certdata()

    @CachedProperty
    def vdom_connector(self):
        logger.debug("Create VDOM connector for {server}: cloud={cloud}, local={local}, internal={internal}".format(
            server = self.server, cloud = self.__is_cloud(self.server),
            local = self.__is_local(self.server), internal = self.__is_internal_auth()))
        if not self.__is_cloud(self.server):
            if not (self.__is_local(self.server) and self.__is_internal_auth()):
                self.server = ensure_https(self.server)
                logger.debug("Modify server: {}".format(self.server))
        else:
            self.prepare_remote_runtime()
            logger.debug("Prepared remote runtime, server={} cloud={}".format(self.server, self.__is_cloud(self.server)))

        sess = VDOMRestSession.create(self.server, self.app_id)
        if not self.__is_https(self.server) and self.__is_cloud(self.server):
            # load SSL certificate data from domain site
            sess.load_certdata(ProMail.promail_domain())
        return sess

    def prepare_remote_runtime(self):
        from appinmail_sso_client import AppinmailClient
        appinmail = AppinmailClient.default()
        args = {
            #'user_email': 'user1@appinmail.io',    # TODO:
            'user_host': self.server
        }
        resp = appinmail.prepare_user_runtime(args)
        self.server = resp['runtime_host']
        if not ProMail.is_cloud_version(request.server.host):
            # for connections to containers in cloud need to
            # remove port from the host name
            self.server = ensure_https(self.server.rsplit(':', 1)[0])

    def remote_login(self, login_container, login_action):
#        user = ProAdmin.current_user()
        user = session.get('current_user')
        token = ProAdmin.access_token()
        token = token or ''
        token_data = token if isinstance(token, basestring) else token.data

        user_email = user.email if user else ''

        self.remote_login_info = {}

        logger.debug(u"EAC login '{}' with token '{}'".format(
                     user_email, token_data))

        resp = self.vdom_connector.call(
            login_container,
            login_action,
            json.dumps({
                'login': user_email,
                'password' : '',
                'token': token_data,
                'eac_token': self.eac_token,
                'sessionToken': self.session_token,
                'caller': self.caller,
                'language': get_lang()
            })
        )

        try:
            status, data = json.loads(resp)

            if status == 'success':
                self.remote_login_info = data
                logger.debug(u'EAC login success: {}'.format(data))

            else:
                self.remote_login_info = {}
                logger.debug(u'EAC login error: {}'.format(resp))

        except: pass
        return resp


    def get_remote_content(self, login_container, login_action,
                           get_container, get_action,
                           pattern, attachments):

        if login_container and login_action:
            self.remote_login(login_container, login_action)

        user = ProAdmin.current_user()
        user_guid = self.remote_login_info.get('guid') or (user and user.guid) or 'None'

        if get_container and get_action:
            body = {
                'sessionToken': self.session_token,
                'required': {
                    'user.guid': user_guid
                },
                'attachments': attachments,
                'caller': self.caller,
                'language': get_lang()
            }

            if pattern:
                body['additional'] = pattern.get('data', '')
                pattern['data'] = body
                pattern = json.dumps(pattern)
            else:
                pattern = json.dumps(body)

            logger.debug(u'GET: {}'.format(pattern))

            response = self.vdom_connector.call(
                get_container,
                get_action,
                pattern
            ).strip()

            if response:
                if response[:20].upper().startswith('<WHOLEXML'):
                    self.wholedata = EACContent(
                        response.encode('utf8')).wholedata
                else:
                    try:
                        response = json.loads(response)
                    except:
                        raise Exception("Can't parse response!")

                    if response[0] == 'error':
                        logger.info(
                            u'EAC.get_remote_content error in response - {}' \
                            .format(str(response[1])))
                        raise Exception(response)

                    self.wholedata = EACContent(
                        response[1].encode('utf8')).wholedata

                self.update_session_token()

                return self.wholedata

        return {}

    def post_to_remote(self, login_container, login_action,
                       post_container, post_action,
                       pattern, data, attachments):
        try:
            return self.__post_to_remote(login_container, login_action,
                                         post_container, post_action,
                                         pattern, data, attachments)
        except Exception as ex:
            if isinstance(ex.message, list) and ex.message[0] == 'error' \
                and ex.message[1] == 2: # not logged in
                logger.debug(u'EAC session expired')
            else:
                raise

        if login_container and login_action:
            self.remote_login(login_container, login_action)

        return self.__post_to_remote(login_container, login_action,
                                     post_container, post_action,
                                     pattern, data, attachments)

    def __post_to_remote(self, login_container, login_action,
                       post_container, post_action,
                       pattern, data, attachments):

        user = ProAdmin.current_user()
        user_guid = self.remote_login_info.get('guid') or (user and user.guid) or 'None'

        if post_container and post_action:
            body = {
                'sessionToken': self.session_token,
                'required': {
                    'user.guid': user_guid
                },
                'trigger': data,
                'attachments': attachments,
                'caller': self.caller,
                'language': get_lang()
            }

            if pattern:
                body['additional'] = pattern.get('data', '')
                pattern['data'] = body
                pattern = json.dumps(pattern)
            else:
                pattern = json.dumps(body)

            logger.debug(u'POST: {}'.format(pattern))

            response = self.vdom_connector.call(
                post_container,
                post_action,
                pattern
            ).strip()

            if response:
                if response[:20].lstrip().upper().startswith('<WHOLEXML'):
                    self.wholedata = EACContent(
                        response.encode('utf8')).wholedata
                else:
                    try:
                        response = json.loads(response)
                    except:
                        raise Exception("Can't parse response!")

                    if response[0] == 'error':
                        logger.info(
                            u'EAC.post_to_remote error in response - {}' \
                            .format(str(response[0])))
                        raise Exception(response)

                    self.wholedata = EACContent(
                        response[1].encode('utf8')).wholedata

                self.update_session_token()

                return self.wholedata

        return {}

    def update_session_token(self):
        new_session_token = self.wholedata['global'].get('SessionToken', None)
        if new_session_token is not None:
            self.session_token = new_session_token
            save_session_token(self.server, self.app_id,
                               self.eac_token, new_session_token)
            response.shared_variables['session_token'] = new_session_token


class EACConnector(BaseEACConnector):

    def __init__(self, wholexml, eac_token, caller='promail'):
        self.eac = EACContent(wholexml.encode('utf8'))
        self.wholedata = self.eac.wholedata
        BaseEACConnector.__init__(self,
            self.wholedata['api']['server'],
            self.wholedata['api']['appID'],
            eac_token,
            self.wholedata['global'].get('SessionToken', ''),
            caller,
            self.wholedata['global'].get('Auth', 'external'))

    def is_static(self):
        return self.eac.is_static()

    def get_content(self, attachments=[]):
        if self.wholedata['vdom']:
            return self.wholedata['vdom']

        return self.get_remote_content(self, attachments)

    def remote_login(self, container, action):
        login = self.wholedata['api']['methods']['login']
        return BaseEACConnector.remote_login(self, login['container'],
                                             login['action'])

    def get_remote_content(self, attachments):
        login = self.wholedata['api']['methods'].get('login', None)
        get = self.wholedata['api']['methods'].get('get', None)
        return BaseEACConnector.get_remote_content(self,
            login['container'] if login else '',
            login['action'] if login else '',
            get['container'] if get else '',
            get['action'] if get else '',
            get.get('pattern', '') if get else '',
            attachments)

    def post_to_remote(self, data, attachments):
        login = self.wholedata['api']['methods'].get('login', None)
        post = self.wholedata['api']['methods'].get('post', None)
        return BaseEACConnector.post_to_remote(self,
            login['container'] if login else '',
            login['action'] if login else '',
            post['container'] if post else '',
            post['action'] if post else '',
            post.get('pattern', '') if post else '',
            data,
            attachments)


class EACObject(object):

    def __init__(self):
        # global
        self.dynamic = True
        self.auth = 'internal'
        self.session_token = ''
        # api
        self.login_container = ''
        self.login_method = ''
        self.get_container = ''
        self.get_method = ''
        self.get_data = ''
        self.post_container = ''
        self.post_method = ''
        self.post_data = ''
        self.api_server = ''
        self.app_id = ''
        # events
        self.events_data = ''
        # vdomxml
        self.vdomxml_data = ''
        # metadata
        self.tags = {}  # name : color
        self.item_plugin = ''
        self.item_vdomxml = ''
        # general
        self.eac_app_name = ''
        self.eac_token = ''
        self.eac_method = ''

    @classmethod
    def from_data(cls, eac_token, payload):
        eac = cls()
        whole = EACContent(payload.encode('utf8')).wholedata
        # global
        glob = whole['global']
        eac.dynamic = (glob.get('Content', '').lower() == 'dynamic')
        eac.auth = glob.get('Auth', 'internal')
        eac.session_token = glob.get('SessionToken', '')
        # api
        api = whole['api']
        login = api['methods'].get('login', None)
        get = api['methods'].get('get', None)
        post = api['methods'].get('post', None)
        eac.login_container = login['container'] if login else ''
        eac.login_method = login['action'] if login else ''
        eac.get_container = get['container'] if get else ''
        eac.get_method = get['action'] if get else ''
        eac.get_data = get.get('pattern', '') if get else ''
        eac.post_container = post['container'] if post else ''
        eac.post_method = post['action'] if post else ''
        eac.post_data = post.get('pattern', '') if post else ''
        eac.api_server = api.get('server', '')
        eac.app_id = api.get('appID', '')
        # events
        eac.events_data = whole['events']
        # vdomxml
        eac.vdomxml_data = whole['vdom']
        # metadata
        tags = whole['metadata'].get('tags', [])
        item = whole['metadata'].get('item', {})
        eac.tags = {}  # name : color
        for t in tags:
            if t.get('name', None) and t.get('color', None):
                eac.tags[t['name']] = t['color']
        eac.item_plugin = item.get('plugin', '') if item else ''
        eac.item_vdomxml = item.get('vdom', '') if item else ''
        # general
        eac.eac_app_name = ''
        eac.eac_token = eac_token
        eac.eac_method = ''
        return eac

    def set_events(self, data):
        """data is dictionary or string (JSON)"""
        self.events_data = data

    def get_eacviewer_url(self, host, email):
        param = {
            'eac_token': self.eac_token,
            'session_token': self.session_token,
            'login_container': self.login_container,
            'login_action': self.login_method,
            'get_container': self.get_container,
            'get_action': self.get_method,
            'post_container': self.post_container,
            'post_action': self.post_method,
            'app_id': self.app_id,
            'server': self.api_server,
            'email': email,
            'pattern': self.get_data if isinstance(self.get_data, basestring) \
                        else json.dumps(self.get_data),
            'pattern_post': self.post_data if isinstance(self.post_data, basestring) \
                        else json.dumps(self.post_data),
            'vdomxml': self.vdomxml_data.encode('utf8') if isinstance(self.vdomxml_data, unicode) else self.vdomxml_data,
            'events': self.events_data,
            'static': '0' if self.dynamic else '1'
        }

        for k in param.keys():
            if not param[k]:
                param.pop(k)

        param = urllib.urlencode(param)

        protocol = 'https'
        if '://' in host:
            protocol, host = host.split('://', 1)

        return urlparse.urlunparse((protocol, host, '/eacviewer', '', param, ''))

    def get_wholexml(self):
        dom_impl = getDOMImplementation()
        doc = dom_impl.createDocument(None, 'WHOLEXML', None)
        root = doc.documentElement
        # root attributes
        root.setAttribute('Content', 'dynamic' if self.dynamic else 'static')
        root.setAttribute('SessionToken', self.session_token)
        root.setAttribute('Auth', self.auth)
        # api
        api = doc.createElement('API')
        api.setAttribute('server', self.api_server)
        api.setAttribute('appID', self.app_id)
        root.appendChild(api)
        # login
        login = doc.createElement('LOGIN')
        login.setAttribute('container', self.login_container)
        login.setAttribute('action', self.login_method)
        api.appendChild(login)
        # get
        get = doc.createElement('GET')
        get.setAttribute('container', self.get_container)
        get.setAttribute('action', self.get_method)
        pattern = doc.createElement('PATTERN')
        get.appendChild(pattern)
        api.appendChild(get)
        if self.get_data:
            self.__append_cdata(doc, pattern, self.get_data)
        # post
        post = doc.createElement('POST')
        post.setAttribute('container', self.post_container)
        post.setAttribute('action', self.post_method)
        pattern = doc.createElement('PATTERN')
        post.appendChild(pattern)
        api.appendChild(post)
        if self.post_data:
            self.__append_cdata(doc, pattern, self.post_data)
        # events
        events = doc.createElement('EVENTS')
        root.appendChild(events)
        if self.events_data:
            self.__append_cdata(doc, events, self.events_data)
        # vdomxml
        vdomxml = doc.createElement('VDOMXML')
        root.appendChild(vdomxml)
        if self.vdomxml_data:
            self.__append_cdata(doc, vdomxml, self.vdomxml_data)
        # metadata
        metadata = doc.createElement('METADATA')
        root.appendChild(metadata)
        tags = doc.createElement('TAGS')
        metadata.appendChild(tags)
        for tag_name in self.tags:
            tag = doc.createElement('TAG')
            tag.setAttribute('name', tag_name)
            tag.setAttribute('color', self.tags[tag_name])
            tags.appendChild(tag)
        if self.item_plugin or self.item_vdomxml:
            item = doc.createElement('ITEM')
            metadata.appendChild(item)
            root.appendChild(metadata)
            plugin = doc.createElement('PLUGIN')
            plugin.setAttribute('id', self.item_plugin)
            item.appendChild(plugin)
            vdomxml = doc.createElement('VDOMXML')
            item.appendChild(vdomxml)
            if self.item_vdomxml:
                self.__append_cdata(doc, vdomxml, self.item_vdomxml)

        return root.toprettyxml(encoding='utf8')
        #return root.toxml(encoding='utf8')

    def __append_cdata(self, doc, elem, data):
        append_cdata(doc, elem,
            json.dumps(data) if isinstance(data, dict) else data)


import ProMail

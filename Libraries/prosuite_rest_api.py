import re
import threading
import urllib
import urllib2
import httplib
import email
import email.utils

from prosuite_logging import app_logger
from prosuite_utils import ensure_https


logger = app_logger.getChild('VDOMAPI')


sid_re = re.compile('sid=(\\w+)')


class ProMailHTTPSConnection(httplib.HTTPSConnection):

    def __init__(self, cert_cb, host, **kwargs):
        self.cert_cb = cert_cb
        httplib.HTTPSConnection.__init__(self, host, **kwargs)

    def connect(self):
        httplib.HTTPSConnection.connect(self)
        if self.cert_cb:
            self.cert_cb(self.sock.getpeercert())


class ProMailHTTPSHandler(urllib2.HTTPSHandler):

    def __init__(self, cert_cb):
        urllib2.HTTPSHandler.__init__(self)
        self.cert_cb = cert_cb

    def https_open(self, req):
        return self.do_open(self.get_connection, req)

    def get_connection(self, host, **kwargs):
        return ProMailHTTPSConnection(self.cert_cb, host, **kwargs)


class VDOMRestSessionClosed(Exception): pass


class CertdataStorage:

    def __init__(self):
        self.__lock = threading.Lock()
        self.__data = {}

    def __key(self, key):
        return key.split("://", 1)[-1].split(":", 1)[0].split("/", 1)[0]

    def put(self, key, certdata):
        with self.__lock:
            self.__data[self.__key(key)] = certdata

    def get(self, key):
        with self.__lock:
            return self.__data.get(self.__key(key), None)


cert_storage = CertdataStorage()


class VDOMRestConnector(object):

    def __init__(self, server, app_id):
        self._original_server = server
        self._server = server
        if self._server.find('//') == -1:
            self._server = 'http://' + self._server
        if not self._server.endswith('/'):
            self._server += '/'
        self._server += 'restapi.py'
        self._app_id = app_id
        self.__sid = ''

    def cert_cb(self, cert):
        logger.debug('Process certificate of {}'.format(self._original_server))
        def _find(seq, name):
            for i in seq:
                if isinstance(i, tuple) \
                    and len(i) > 0 \
                    and isinstance(i[0], tuple) \
                    and len(i[0]) > 1 \
                    and i[0][0] == name:
                    return i[0][1]
            return ''
        def _format_time(t):
            ret = email.utils.parsedate(t)
            if ret:
                return '{}/{}/{}'.format(ret[2], ret[1], ret[0])
            else:
                return ''
        certification = _find(cert.get('issuer', []), 'commonName')[:25]
        sender = _find(cert.get('subject', []), 'commonName')
        if certification and sender:
            certdata = {
                'sender': sender,
                'certification': certification,
                'valid_from': _format_time(cert.get('notBefore', '')),
                'valid_to': _format_time(cert.get('notAfter', ''))
            }
            cert_storage.put(self._original_server, certdata)
            logger.debug(' '.join([self._original_server, certification, sender]))
        else:
            logger.debug('Certificate of {} has no information'.format(self._original_server))

    def load_certdata(self, domain):
        if not cert_storage.get(self._original_server):
            url = 'eacviewer.' + domain
            certdata = cert_storage.get(url)
            if certdata:
                cert_storage.put(self._original_server, certdata)
                return
            logger.debug("Try to load SSL certificate from {}".format(url))
            try:
                req = urllib2.Request(url='https://' + url)
                opener = urllib2.build_opener(ProMailHTTPSHandler(self.cert_cb))
                f = opener.open(req)
            except Exception as ex:
                logger.debug('Error loading certificate from {}: {}'.format(url, ex))
            certdata = cert_storage.get(self._original_server)
            if certdata:
                cert_storage.put(url, certdata)

    def __find_sid(self, headers):
        for h in headers:
            if h.lower().startswith('set-cookie:'):
                sid = str(sid_re.search(h, 1).group(1))
                if sid:
                    return sid
        return self.__sid

    def call(self, container, action, param):
        data = {
         "appid" : self._app_id,
         "objid" : container,
         "action_name" : action,
         "xml_data" : param
        }
        req = urllib2.Request(url=self._server, data=urllib.urlencode(data))
        if self.__sid:
            req.add_header('Cookie', 'sid={}'.format(self.__sid))
        opener = urllib2.build_opener(ProMailHTTPSHandler(self.cert_cb))
        f = opener.open(req)
        self.__sid = self.__find_sid(f.info().headers)
        logger.debug('Call {}: {}'.format(action, f.getcode()))
        return f.read().decode('utf8')


KEY = 'VDOM_REST_API_SESSIONS'


class VDOMRestSession(object):

    GLOB_SEM = threading.Semaphore()

    def __init__(self, server, app_id):
        self._server = server
        self._app_id = app_id
        self._api = None

    def get_certdata(self):
        certdata = cert_storage.get(self._server)
        return certdata if certdata and certdata['certification'] != '' else None

    def load_certdata(self, domain):
        self.api().load_certdata(domain)

    def api(self):
        if not self._api:
            self._api = VDOMRestConnector(self._server, self._app_id)
        return self._api

    def call(self, *args, **kwargs):
        try:
            return self.api().call(*args, **kwargs)
        except Exception as ex:
            key = self._server + self._app_id
            logger.debug('Session {} closed: {}'.format(key, ex))
            session.get(KEY, {}).pop(key, None)
            raise VDOMRestSessionClosed

    @classmethod
    def create(cls, server, app_id):
        cls.GLOB_SEM.acquire()
        try:
            sessions = session.get(KEY, {})
            key = server + app_id
            if key not in sessions:
                logger.debug('New session created: ' + key)
                sessions[key] = cls(server, app_id)
            else:
                logger.debug('Existing session found: ' + key)
            session[KEY] = sessions
            return sessions[key]
        finally:
            cls.GLOB_SEM.release()

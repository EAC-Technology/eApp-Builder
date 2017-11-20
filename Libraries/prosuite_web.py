"""
ProSuite Web Utils and Classes
"""

import md5
import threading
import time
import urlparse

from collections import defaultdict, OrderedDict
from functools import wraps
from urllib import urlencode
from UserDict import DictMixin
from uuid import uuid4

#from promail_tasks import tasks
from prosuite_errors import ProSuiteBaseError
from prosuite_localization import get_localization
from prosuite_logging import app_logger
from prosuite_settings import settings
from prosuite_user import ProSuiteUser
from prosuite_utils import CachedProperty




##############################
#
# Global Private Constants
#
##############################

# Default value for function arguments
_DEFAULT_VALUE = []

# Growl types
_GROWL_TYPES = ("show", "showInformation", "showWarning", "showError")

# Cookie max age
_COOKIE_MAX_AGE = str(60 * 60 * 24 * 365)



##############################
#
# Module Exceptions
#
##############################

class MissingRequestDataError(KeyError):
    """
    Missing Data in Request Error
    """
    pass


class MissingArgumentError(MissingRequestDataError):
    """
    Missing request argument error
    """
    pass


class MissingSharedVariableError(MissingRequestDataError):
    """
    Missing shared variable error
    """
    pass


class MissingCookieError(MissingRequestDataError):
    """
    Missing cookie error
    """
    pass


class RequestSessionError(Exception):
    """
    Request session error
    """
    pass


class RequestSessionDoesntExist(RequestSessionError):
    """
    Request session not exists
    """
    pass


class RequestSessionInvalidKey(RequestSessionError):
    """
    Request session not exists
    """
    pass


class RedirectException(Exception):
    """
    Redirect exception
    """
    def __init__(self, redirect_to, params=None, back_url=""):
        super(RedirectException, self).__init__()
        self.back_url = back_url
        self.params = params
        self.redirect_to = redirect_to




##############################
#
# Request Storage Implemeation
#
##############################

class RequestStorageMeta(type):
    """
    Request Storage Meta Class
    """
    def __new__(mcs, classname, bases, classDict):

        # handler prefixes
        prefixes = ("get", "set", "del")
        handlers_attr_t = "%s_handlers"
        func_attr_t = "%s_key"

        for prefix in prefixes:

            h_attr = handlers_attr_t % prefix
            f_attr = func_attr_t % prefix

            handlers = classDict[h_attr] = {}

            for base in bases:
                handlers.update(getattr(base, h_attr, {}))

            for item in classDict.itervalues():
                if hasattr(item, f_attr):
                    handlers[getattr(item, f_attr)] = item

        return type.__new__(mcs, classname, bases, classDict)


class RequestStorage(dict):

    __metaclass__ = RequestStorageMeta

    @staticmethod
    def get_handler(key):
        """
        Decorator to mark method as missing key handler
        """
        def wrapper(func):
            func.get_key = key
            return func

        return wrapper

    @staticmethod
    def set_handler(key):
        """
        Decorator to mark method as set key handler
        """
        def wrapper(func):
            func.set_key = key
            return func

        return wrapper

    @staticmethod
    def del_handler(key):
        """
        Decorator to mark method as del key handler
        """
        def wrapper(func):
            func.del_key = key
            return func

        return wrapper

    def __init__(self, delegate, *args, **kwargs):
        super(RequestStorage, self).__init__(*args, **kwargs)
        self.delegate = delegate

    def __missing__(self, key):
        if key not in self.get_handlers:
            raise KeyError(key)

        value = self.get_handlers[key](self)
        super(RequestStorage, self).__setitem__(key, value)
        return value

    def __setitem__(self, key, value):
        super(RequestStorage, self).__setitem__(key, value)
        if key in self.set_handlers:
            self.set_handlers[key](self, value)

    def __delitem__(self, key):
        value = super(RequestStorage, self).pop(key, None)
        if key in self.del_handlers:
            self.del_handlers[key](self, value)

    get_by_key = dict.__getitem__
    del_by_key = dict.__delitem__
    set_by_key = dict.__setitem__


##############################
#
# Request session
#
##############################

class RequestSession(dict):

    def __init__(self):
        super(RequestSession, self).__init__()
        self._last_access = time.time()

    @property
    def last_access(self):
        return self._last_access

    def touch(self):
        self._last_access = time.time()


class RequestSessionManager(object):

    GLOB_LOCK = threading.Lock()
    TIMEOUT = 60.0 * 3

    def __init__(self):
        self._request_sessions = {}

    def count(self):
        """
        Return count of registered instances
        """
        return len(self._request_sessions)

    def remove_expired(self):
        """
        Remove expired instances from dict
        """
        now = time.time()
        return [self.remove_if_expired(key, now) for key in self._request_sessions.keys()[:]].count(True)

    def remove_if_expired(self, key, now):
        """
        Remove instance from dict if expired
        """
        with self.GLOB_LOCK:
            inst = self._request_sessions.get(key, None)
            if inst is not None and (inst.last_access + self.TIMEOUT < now):
                self._request_sessions.pop(key, None)
                return True

            return False

    def remove_request_session(self, key):
        """
        Remove instance from dict
        """
        with self.GLOB_LOCK:
            return self._request_sessions.pop(key, None)

    def get_request_session(self, key):
        """
        Return instance from dict if exists
        """
        with self.GLOB_LOCK:
            inst = self._request_sessions.get(key, None)
            if inst is not None:
                inst.touch()

            return inst

    def pop_request_session(self, key):
        """
        Remove instance from dict and return it
        """
        with self.GLOB_LOCK:
            inst = self._request_sessions.pop(key, None)
            if inst is not None:
                inst.touch()

            return inst

    def put_request_session(self, key, inst):
        """
        Put instance to dict
        """
        with self.GLOB_LOCK:
            inst.touch()
            self._request_sessions[key] = inst

    def create_request_session(self):
        """
        Return new instance
        """
        return RequestSession()


RequestSessionManager = RequestSessionManager()



##############################
#
# Shared Variables Implemetation
#
##############################

class SharedVariables(DictMixin):

    def __init__(self):
        # copy all existing SVs in request
        sv = request.shared_variables
        self.data = {key: sv[key] for key in sv.keys()}

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
        response.shared_variables[key] = value

    def __delitem__(self, key):
        # silently delete value by key
        self.data.pop(key, None)
        try:
            del response.shared_variables[key]
        except:
            pass




##############################
#
# Helpers Functions
#
##############################
def message_to_ul_li(msg):
    if isinstance(msg, (list, tuple)):
        msg = u"<ul>{}</ul>".format(u"".join([
            u"<li>{}</li>".format(item) for item in msg
        ]))

    return msg



##############################
#
# Callbacks logic implemetation
#
##############################

def callback(name, order=0):
    """
    Decorator to mark method as callback
    """
    def decorator_func(func):
        if not hasattr(func, "_callbacks"):
            func._callbacks = defaultdict(list)

        func._callbacks[name].append(order)
        return func

    if callable(name):
        func = name
        name = func.__name__
        return decorator_func(func)

    return decorator_func


class BasePageMetaClass(type):
    """
    Metaclass for Page Controllers
    """
    def __new__(mcs, classname, bases, classDict):

        # callbacks will have structure like
        # {
        #   "callback_name": {
        #       1: func_1,
        #       10: func_2
        #   }
        # }
        callbacks = {}

        # check callbacks in parent classes
        for base in bases:

            if not (hasattr(base, "callbacks") and base.callbacks):
                continue

            for name in base.callbacks:
                if name not in callbacks:
                    callbacks[name] = {}

                callbacks[name].update(base.callbacks[name])

        # check callbacks in new class
        for item in classDict.itervalues():

            if not hasattr(item, "_callbacks"):
                continue

            for name, order in item._callbacks.items():
                if name not in callbacks:
                    callbacks[name] = {}

                for i in order:
                    callbacks[name][i] = item

                callbacks[name] = OrderedDict(sorted(callbacks[name].items(), key=lambda x: x[0]))

        classDict["callbacks"] = callbacks
        return super(BasePageMetaClass, mcs).__new__(mcs, classname, bases, classDict)


class BasePageController(object):

    __metaclass__ = BasePageMetaClass

    def __init__(self, page):

        # current action name
        self._action_name = ""

        # current user
        self._current_user = None

        # logger
        self._logger = None

        # is action mode
        self._is_action = None

        # page object
        self._page = page

        # shared vars
        self._shared_vars = SharedVariables()

        # dictionary with VDOM objects
        self.vdom_objects = {}

        # init functions depends on request mode
        self._init_implementation()

    ###########################################
    # <<<<<<<<<<<< Properties >>>>>>>>>>>>>>> #
    ###########################################

    @property
    def action_name(self):
        return self._action_name

    @property
    def app_settings(self):
        return self.get_application_settings()

    @property
    def current_user(self):
        if self._current_user is None:
            self._current_user = self.get_current_user()

        return self._current_user

    @property
    def logger(self):
        if self._logger is None:
            self._logger = app_logger.getChild("Pages").getChild(self.__class__.__name__)

        return self._logger

    @property
    def page(self):
        return self._page

    @property
    def shared_vars(self):
        return self._shared_vars

    @property
    def request_session_manager(self):
        return RequestSessionManager


    ###########################################
    # <<<<<<<< Methods to override >>>>>>>>>> #
    ###########################################

    def get_application_settings(self):
        raise NotImplementedError

    def get_current_user(self):
        raise NotImplementedError

    def get_home_url(self):
        raise NotImplementedError

    def get_localization(self):
        raise NotImplementedError

    def get_localization_data(self):
        raise NotImplementedError

    def get_login_url(self):
        raise NotImplementedError

    def get_logout_url(self):
        raise NotImplementedError

    def is_debug(self):
        raise NotImplementedError

    ###########################################
    # <<<<<<<<<<<<< Main logic >>>>>>>>>>>>>> #
    ###########################################

    def execute_callbacks(self, name, *args, **kwargs):
        """
        Call registered callbacks by name
        """
        callbacks = self.callbacks.get(name, {}).items()
        for order, func in callbacks:
            func(self, *args, **kwargs)

        return len(callbacks)

    def run(self, action):
        """
        Run request processing
        """
        self._action_name = action
        self._work()

    def _work(self):
        """
        Main logic
        """
        try:
            self.execute_callbacks('request_start', action=self._action_name)
            self.execute_callbacks(self._action_name)

        finally:
            self.execute_callbacks('request_done', action=self._action_name)

    ###########################################
    # <<<<<<<<< Localization logic >>>>>>>>>> #
    ###########################################

    @CachedProperty
    def localization(self):
        return self.get_localization()

    def localize_page(self):
        self.localization.controls = self.get_localization_data()
        self.localization.localize()

    ###########################################
    # <<<<<<<<<<<<< Request info >>>>>>>>>>>> #
    ###########################################

    def get_shared_var(self, key, default=_DEFAULT_VALUE, strip=False):
        value = request.shared_variables[key] or default
        if value is _DEFAULT_VALUE:
            raise MissingArgumentError(key)

        return value.strip() if strip else value

    def set_shared_var(self, key, value):
        response.shared_variables[key] = value

    def del_shared_var(self, key):
        del response.shared_variables[key]

    def current_protocol(self):
        if request.environment.get("SERVER_PORT", "80") == "443":
            return "https"

        return request.protocol.name.lower()

    def current_host(self):
        return request.server.host

    def current_page(self):
        uri = request.environment.get("REQUEST_URI", "")
        referer = request.environment.get("HTTP_REFERER", "")

        try:
            return urlparse.urlsplit(referer if self.is_action() else uri).path
        except:
            return ""

    def current_page_id(self):
        return request.container.id

    def current_protocol(self):
        if request.environment.get("SERVER_PORT", "80") == "443":
            return "https"

        return request.protocol.name.lower()

    def current_query( self ):
        try:
            return request.environment.get("QUERY_STRING", "")
        except:
            return ""

    def current_uri( self ):
        query = self.current_query()
        if query:
            return self.current_page() + '?' + query
        return self.current_page()

    def full_url( self ):
        return self.current_protocol() + "://" + self.current_host() +\
                self.current_page() + "?" + self.current_query()

    def is_action(self):
        if self._is_action is None:
            try:
                self._is_action = request.render_type == "e2vdom"

            except:
                self._is_action = False

        return self._is_action

    ###########################################
    # <<<<<<<<<<<< Redirect logic >>>>>>>>>>> #
    ###########################################

    def generate_redirect_url(self, url, params=None, back_url=""):
        """
        Generate redirect URL
        """
        params = params or {}

        if back_url:
            params["back_url"] = back_url

        url = urlparse.urlsplit(url)

        return u"{scheme}{netloc}{path}{question}{query}{concat}{params}{fragment}".format(
            scheme = (url.scheme + u"://") if url.scheme else u"",
            netloc = url.netloc,
            path   = url.path,
            query  = url.query,
            fragment = (u"#" + url.fragment) if url.fragment else u"",
            concat = u"" if not params else u"&" if url.query else u"?",
            question = u"" if not url.query else u"?",
            params = urlencode(params)
        )

    def redirect(self, redirect_to, params=None, back_url="", terminate=False):
        """
        Redirect to URL and generate back URL
        """
        if params or back_url:
            redirect_to = self.generate_redirect_url(redirect_to, params, back_url)

        if terminate:
            raise RedirectException(redirect_to)

        if self.is_action():
            self.page.action('goTo', [redirect_to])

        else:
            response.redirect(redirect_to)

    ###########################################
    # <<<<<<<<<< Render mode impl >>>>>>>>>>> #
    ###########################################

    def _init_implementation(self):
        if self.is_action():
            self.show_object = self.show_object_action
            self.hide_object = self.hide_object_action
            self.show_growl = self.show_growl_action

        else:
            self.show_object = self.show_object_onload
            self.hide_object = self.hide_object_onload
            self.show_growl = self.show_growl_onload

    def show_object_action(self, vdom_object):
        vdom_object.action("show", [""])

    def show_object_onload(self, vdom_object):
        vdom_object.visible = "1"

    def hide_object_action(self, vdom_object):
        vdom_object.action("hide", [""])

    def hide_object_onload(self, vdom_object):
        vdom_object.visible = "0"

    def show_growl_action(self, msg, title="", growl_t="show"):
        self.growl.action(growl_t, [title, message_to_ul_li(msg), False])

    def show_growl_onload(self, msg, title="", growl_t="show"):
        self.growl.title = title
        self.growl.text = message_to_ul_li(msg)
        self.growl.active = "1"
        self.growl.style = _GROWL_TYPES.index(growl_t)

    ###########################################
    # <<<<<<<<< Growl Notification >>>>>>>>>> #
    ###########################################

    @property
    def growl(self):
        return self.vdom_objects["growl"]

    def show_error_growl(self, text, title=""):
        self.show_growl(growl_t="showError", msg=text, title=title)

    def show_info_growl(self, text, title=""):
        self.show_growl(growl_t="showInformation", msg=text, title=title)

    def show_warning_growl(self, text, title=""):
        self.show_growl(growl_t="showWarning", msg=text, title=title)

    ###########################################
    # <<<<<<<<<<<<< Request args >>>>>>>>>>>> #
    ###########################################

    def get_argument(self, key, default=_DEFAULT_VALUE, strip=True, castto=None):
        value = request.arguments.get(key, default=default, castto=castto)
        if value is _DEFAULT_VALUE:
            raise MissingArgumentError(key)

        return value.strip() if strip and value is not default else value

    def get_cookie(self, key, default=_DEFAULT_VALUE):
        key = key.encode("utf8")
        value = request.cookies.get(key)
        if value is None and default is _DEFAULT_VALUE:
            raise MissingCookieError(key)

        return value.value if value else default

    def set_cookie(self, key, value, age=_COOKIE_MAX_AGE, **kwargs):
        key = key.encode("utf8")
        response.cookies[key] = value
        response.cookies[key]['max-age'] = age

        for arg in kwargs:
            response.cookies[key][arg] = kwargs[key]

    def del_cookie(self, key):
        key = key.encode("utf8")
        response.cookies.pop(key, None)


##############################
#
# Decorators
#
##############################

def authenticated(method):
    """authenticated decorator
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs ):
        if not self.current_user:
            # redirect to login page
            raise RedirectException(self.get_login_url(), back_url=self.current_uri())

        return method(self, *args, **kwargs)

    return wrapper


def administrator_only(method):
    """authenticated decorator
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs ):
        if not self.current_user.is_admin():
            # redirect to login page
            raise RedirectException(self.get_home_url())

        return method(self, *args, **kwargs)

    return wrapper


def error_handler(method):
    """error handler decorator
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)

        except RedirectException as ex:
            self.redirect(
                ex.redirect_to,
                back_url=ex.back_url,
                params=ex.params
            )

        except MissingRequestDataError:
            if self.is_debug():
                raise

            self.show_error_growl(
                self.localization["global.invalid_request.text"],
                self.localization["global.invalid_request.title"]
            )

        except RequestSessionError as ex:
            self.show_error_growl(
                self.localization["global.invalid_request_session.text"],
                self.localization["global.invalid_request_session.title"]
            )

        except ProSuiteBaseError as ex:
            if not self.execute_callbacks('request_failed', exc=ex) and self.is_debug():
                raise

        except Exception as ex:

            eid = uuid4().hex[:6]
            self.logger.exception("[EID=%s] Unhandled exception caught!!!", eid)
            if self.is_debug():
                raise

            self.redirect(self.get_server_500_error_url(), params={
                'eid': eid,
                'back_url': self.current_uri()
            })

    return wrapper


class ProSuiteBasicPage(BasePageController):

    def get_application_settings(self):
        return settings

    def get_current_user(self):
        return ProSuiteUser.current_user()

    def get_home_url(self):
        return self.app_settings.pages["home"]

    def get_localization(self):
        return get_localization()

    def get_login_url(self):
        return self.app_settings.pages["login"]

    def get_logout_url(self):
        return self.app_settings.pages["logoff"]

    def get_page_title(self):
        raise NotImplementedError

    def get_server_500_error_url(self):
        return self.app_settings.pages["server500"]

    def is_debug(self):
        return self.app_settings.system["debug"]

    def localize_page(self):
        self.page.title = self.app_settings.localization["page_title"].format(
            app_name=self.app_settings.info["name"],
            page_name=self.get_page_title()
        )
        super(ProSuiteBasicPage, self).localize_page()



    def compute_request_session_key(self, uuid):
        return md5.new("".join([
            session.id,
            self.current_user.guid if self.current_user else "",
            self.page.name,
            uuid
        ])).hexdigest()

    def generate_request_session_key(self):
        """
        Generate unique request session key
        """
        uuid = uuid4().hex
        return self.compute_request_session_key(uuid), uuid

    def verify_request_session_key(self, key, uuid):
        """
        Generate unique request session key
        """
        return self.compute_request_session_key(uuid) == key

    @property
    def request_session(self):
        """
        If session not fetched - fetch its SID from shared vars
        then try to find session, if session not exists:
        1. if it is action - show growl and refresh page
        2. if it is onload - create new instance
        """
        if not hasattr(self, "_request_session"):
            rqsid = self.shared_vars.pop("rqsid", "")
            rqses = self.request_session_manager.pop_request_session(rqsid)

            if not rqses:
                if self.is_action():
                    del session['VDOM_API_SESSIONS']
                    raise RequestSessionDoesntExist

                rqses = self.request_session_manager.create_request_session()

            else:
                uuid = rqses["rqsid_uuid"]
                if not self.verify_request_session_key(rqsid, uuid):
                    del session['VDOM_API_SESSIONS']
                    raise RequestSessionInvalidKey

            self._request_session = rqses

        return self._request_session

    def has_request_session(self):
        return hasattr(self, "_request_session")

    @callback("request_done", 1)
    def save_request_session(self, *args, **kwargs):
        if self.has_request_session():
            key, uuid = self.generate_request_session_key()
            self.request_session["rqsid_uuid"] = uuid
            self.shared_vars["rqsid"] = key
            self.request_session_manager.put_request_session(key, self.request_session)


    @error_handler
    def run(self, *args, **kwargs):
        super(ProSuiteBasicPage, self).run(*args, **kwargs)

    @callback("onload", 1)
    def onload_localization(self, *args, **kwargs):
        self.localize_page()



#######################################
# Cleaner task - remove expired request session storage
# unique task (it means it will have only single record for given set of params)
# repeat it every 20 minutes

TASK_TIMEOUT = RequestSessionManager.TIMEOUT


#@tasks.background_other(unique=True, repeat_every=TASK_TIMEOUT, repeat_times=-1)
def clean_request_sessions():

    app_logger.getChild("RQSClenaer").debug(
        "RQS task done, %d removed", RequestSessionManager.remove_expired()
    )


clean_request_sessions()




import managers
import re
from uuid import uuid4

RES_CACHE_KEY = "resource_cache"


class resource_cache:

    @property
    def __cache(self):
        c = session.get(RES_CACHE_KEY, None)
        if c is not None:
            return c
        session[RES_CACHE_KEY] = {}
        return session.get(RES_CACHE_KEY)


    def get_resource(self, guid):
        sess = managers.request_manager.current.session()
        return sess.files.get(guid, None)


    def put_resource(self, guid, value):
        sess = managers.request_manager.current.session()
        sess.files[guid] = value


    def guid_by_url(self, url):
        return self.__cache.get(url, None)


    def url_by_guid(self, guid):
        return self.__cache.get(guid, None)


    def add_url(self, url):
        guid = str(uuid4())
        cache = self.__cache
        cache[url] = guid
        cache[guid] = url
        return guid


cache = resource_cache()


def replace_resource_links(str_data, server_addr, re_obj=None, protocol="http",
                           index=None):
    if not re_obj:
        if not server_addr:
            return str_data
        re_obj = re.compile("(http(s)?://)?" + server_addr + "[^\'\"\\s\\[\\]]+")

    def repl_func(matchobj):
        groups = matchobj.groups()
        if index is not None:
            url = groups[index] if groups and len(groups) > index and groups[index] else None
            if not url:
                return matchobj.group(0)
        else:
            url = matchobj.group(0)
        if url.endswith("#nocache"):
            return url[:-8]
        if server_addr not in url:
            url = protocol + "://" + server_addr + url
        guid = cache.guid_by_url(url)
        if not guid:
            guid = cache.add_url(url)
        return "/cached_resource.vdom?r={}".format(guid)

    return re_obj.sub(repl_func, str_data)



RE_OBJ_RES = re.compile("[\'\"](/[\\w\\-]+\\.(res|png|jpg|jpeg|gif)[^\'\"\\s]*)[\'\"]")
RE_PLUGIN_RES = re.compile("[\'\"](/get_plugin_resource\\?[\\w\\-\\&\\=\\.]+)[\'\"]")


def replace_all_resource_links(str_data, server_addr, protocol="http"):
    str_data = replace_resource_links(str_data, server_addr)
    str_data = replace_resource_links(str_data, server_addr, RE_OBJ_RES,
                                      protocol, index=0)
    str_data = replace_resource_links(str_data, server_addr, RE_PLUGIN_RES,
                                      protocol, index=0)
    return str_data



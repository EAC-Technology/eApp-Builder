import managers
import urllib2, tempfile, ssl
import resource_cache
from utils.file_argument import File_argument
from prosuite_logging import app_logger
import ProMail

logger = app_logger.getChild("RES_CACHE")

res_id = request.arguments.get('r')

if not res_id:
    raise ValueError("Parameter required")

res_url = resource_cache.cache.url_by_guid(res_id)
if not res_url:
    # Incorrect resource ID
    response.send_htmlcode(404)


unwanted_headers = ['transfer-encoding', 'set-cookie']


def make_headers(headers_list):
    ret = {}
    for h in headers_list:
        header = h.split(':', 1)
        if len(header) == 2 and header[0].lower() != 'set-cookie':
            ret[header[0]] = header[1].strip()
    return ret


try:
    res = resource_cache.cache.get_resource(res_id)
    if res:
        headers = res.headers
        f = open(res.fileobj.name, "rb")
        content = f.read()
        f.close()
        logger.debug("Serve resource {} from cache".format(res_id))
    else:
        if ProMail.is_cloud_version():
            if '?' not in res_url:
                res_url += '?'
            else:
                res_url += '&'
            res_url += "internal=1"
        logger.debug("Download resource {} ({})".format(res_id, res_url))
        ssl._create_default_https_context = ssl._create_unverified_context
        res_request = urllib2.Request(url=res_url)
        if 'pisid' in request.cookies:
            res_request.add_header("Cookie", "pisid={};".format(request.cookies['pisid'].value))
        if 'dport' in request.cookies:
            res_request.add_header("Cookie", "dport={};".format(request.cookies['dport'].value))
        resp = urllib2.urlopen(res_request)
        if resp.getcode() != 200:
            raise RuntimeError("Remote server response code {}".format(resp.getcode()))
        headers = make_headers(resp.info().headers)
        content = resp.read()
        temp_file = tempfile.NamedTemporaryFile("w+b", prefix="eacrescache", dir=VDOM_CONFIG["TEMP-DIRECTORY"], delete=False)
        temp_file.write(content)
        temp_file.close()
        res = File_argument(temp_file, "")
        res.autoremove = False
        setattr(res, "headers", headers)
        resource_cache.cache.put_resource(res_id, res)
        logger.debug("Save resource {} in cache".format(res_id))

    managers.request_manager.current.headers_out().dict = {}
    resp_headers = response.headers
    for h in headers:
        if h.lower() in unwanted_headers:
            continue
        resp_headers[h] = headers[h]
    response.binary = True
    response.nocache = True
    response.write(content)

except Exception as e:
    #response.write(str(e))
    debug(str(e))
    raise

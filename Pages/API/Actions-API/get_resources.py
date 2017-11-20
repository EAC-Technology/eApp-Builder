import managers
from api_helper import *
from base64 import b64encode

@error_handler
def main():
    try:
        lst = []
        res_id = request.arguments.get('xml_data').split(',')
        for id in res_id:
            r = managers.resource_manager.get_resource(None, id)
            if r:
                lst.append(r)
        write_response('<Resources>' + '\n'.join(['<Resource id="{}">{}</Resource>'.format(r.id, b64encode(r.get_data())) for r in lst]) + '</Resources>')
    except Exception as e:
        debug(str(e))
        raise

main()

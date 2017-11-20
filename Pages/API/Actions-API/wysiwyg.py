import managers
from api_helper import *

@error_handler
def main():
    try:
        p = request.arguments.get('xml_data').split(' ', 1)
        obj = self.loads(p[1])
        result = managers.engine.wysiwyg(obj, self)
        write_response(p[0] + ' ' + result)

    except Exception as e:
        debug(str(e))
        raise

main()

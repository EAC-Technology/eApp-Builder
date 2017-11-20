from api_helper import *
from base64 import b64decode
@error_handler
def main():

    try:
        p = request.arguments.get('xml_data').split('\n')
        ret = []
        for i in range(len(p)):
            if i % 2:
                ret.append(application.resources.create_temporary(self.id, p[i-1], b64decode(p[i])))
            else:
                ret.append(p[i])
        write_response('\n'.join(ret))

    except Exception as e:
        debug(str(e))
        raise

main()

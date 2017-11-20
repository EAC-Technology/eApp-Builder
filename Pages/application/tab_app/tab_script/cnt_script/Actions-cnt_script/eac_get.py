from promail_eac_helper import eacviewer_authenticated, read_attachments, \
                               read_pattern, read_params, EACVIEWER, \
                               process_vdomxml_resources
from promail_eac import BaseEACConnector

from vdom_debug import *

#@eacviewer_authenticated
def main():
    params = read_params()
    attachments = read_attachments()
    pattern = read_pattern()
    try:
        eac = BaseEACConnector(params['server'], params['app_id'],
                               params['eac_token'], params['session_token'],
                               caller=EACVIEWER) #TODO: auth
        wholedata = eac.get_remote_content(params['login_container'],
                                           params['login_action'],
                                           params['get_container'],
                                           params['get_action'],
                                           pattern,
                                           attachments)

        if 'vdom' in wholedata:
            self.dialog_preview.eacviewer.vdomxml = process_vdomxml_resources(eac)
            if wholedata['events']:
                self.dialog_preview.eacviewer.vdomactions = wholedata['events']

    except Exception as ex:
#        response.write(str(ex))
        debug(str(ex))
        r(exception_trace())
        raise

try:
    main()
except:
    # Workaround situation when remote container hasn't compiled macros.
    # In this case repeated request should succeed.
    import time
    time.sleep(5)
    main()

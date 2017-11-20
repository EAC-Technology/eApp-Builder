import json

from promail_eac import BaseEACConnector
from promail_eac_helper import eacviewer_authenticated, read_attachments, \
                               read_pattern, read_params, EACVIEWER, \
                               process_vdomxml_resources

#@eacviewer_authenticated
def main():
    params = read_params()
    attachments = read_attachments()
    pattern = read_pattern('pattern_post')
    try:
        data = {
            "name": request.arguments["customName"],
            "params": json.loads(request.arguments["parameters"])
        }
        eac = BaseEACConnector(params['server'], params['app_id'],
                               params['eac_token'], params['session_token'],
                               caller=EACVIEWER) #TODO: auth
        wholedata = eac.post_to_remote(params['login_container'],
                                       params['login_action'],
                                       params['post_container'],
                                       params['post_action'],
                                       pattern,
                                       data,
                                       attachments)

        if 'vdom' in wholedata:
            sel.dialog_previewf.eacviewer.vdomxml = process_vdomxml_resources(eac)
            if wholedata['events']:
                self.dialog_preview.eacviewer.vdomactions = wholedata['events']

    except Exception as ex:
        #response.write(str(ex))
        debug(str(ex))
        raise

main()

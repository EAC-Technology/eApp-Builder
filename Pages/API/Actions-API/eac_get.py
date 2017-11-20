from api_helper import *
from promail_eac import EACConnector

@authenticated
@error_handler
@parse_json
def main(data):

    eac_content = data.get("eac_content", "")
    eac_token = data.get("eac_token", "")
    if not eac_content or not eac_token:
        raise APICallFailedException("errParameterRequired")
    attachments = data.get("attachments", [])

    try:
        eac = EACConnector(eac_content, eac_token)
        wholedata = eac.get_remote_content(attachments)

        result = u""

        if 'vdom' in wholedata:
            self.eacviewer.vdomxml = wholedata['vdom']
            if wholedata['events']:
                self.eacviewer.vdomactions = wholedata['events']
            result = self.render(None)

        write_response(result)

    except Exception as e:
        #response.write(str(e))
        debug(str(e))
        raise

main()

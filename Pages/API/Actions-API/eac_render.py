from api_helper import *

@error_handler
@parse_json
def main(data):

    eac_vdomxml = data.get("eac_vdomxml", "")
    if not eac_vdomxml:
		raise APICallFailedException("errParameterRequired")

    eac_event = data.get("eac_event", "")

    try:
        result = u""

        self.eacviewer.vdomxml = eac_vdomxml
        self.eacviewer.vdomactions = eac_event
        result = self.render(None)

        write_response(result)

    except Exception as e:
        #response.write(str(e))
        debug(str(e))
        raise

main()

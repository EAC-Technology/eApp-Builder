import json

from prosuite_logging import app_logger
from prosuite_rest_api import VDOMRestConnector
from promail_eac import EACContent

import ProAdmin

logger = app_logger.getChild("EAC")

API_ID = "5073ff75-da99-44fb-a5d7-e44e5ab28598"

class PromailEACRenderer:

    @staticmethod
    def session():
        return VDOMRestConnector('127.0.0.1',
            'dbf4ed0c-969e-4235-98c9-b9b7c84e1b3f')

    @staticmethod
    def make_response(resp):
        resp = json.loads(resp)
        if resp[0] == 'success':
            return resp[1]
        raise RuntimeError(resp[1])

    @staticmethod
    def render(mailbox_creator_uuid, eac_content, eac_token, attachments=[]):
        eac = EACContent(eac_content.encode("utf8"))

        eac_vdomxml = eac.wholedata["vdom"]
        eac_event = eac.wholedata["events"] if eac.wholedata["events"] else ""

        sess = PromailEACRenderer.session()

        if eac.wholedata['global']['Content'].lower() == "static":
            pattern = json.dumps({ "eac_vdomxml": eac_vdomxml,
                                   "eac_event": eac_event })
            resp = sess.call(API_ID, "eac_render", pattern)
        else:
            user = ProAdmin.application().get_users(guid=mailbox_creator_uuid)[0]
            pattern = json.dumps({ "login": user.email,
                                   "token": ProAdmin.sudo_accesstoken(user) })
            login = sess.call(API_ID, "login", pattern)
            pattern = json.dumps({ "eac_content": eac_content,
                                   "eac_token": eac_token,
                                   "attachments": attachments })
            resp = sess.call(API_ID, "eac_get", pattern)

        return PromailEACRenderer.make_response(resp)

    @staticmethod
    def render_vdomxml(eac):
        if not eac.wholedata["vdom"]:
            return ""
        pattern = json.dumps({ "eac_vdomxml": eac.wholedata["vdom"],
                               "eac_event": eac.wholedata["events"] if eac.wholedata["events"] else "" })
        return PromailEACRenderer.make_response(
            PromailEACRenderer.session().call(API_ID, "eac_render", pattern))

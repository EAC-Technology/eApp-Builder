"""
	View model
"""
import lxml.etree as ET
import json

from utils_base_classes import SoftDeletionModel, cached_property
from model_application import Application
from model_acl import acl_mixin, Role, Right
from model_widget import Widget


class View(SoftDeletionModel, acl_mixin):

	db_table = 'eapp_view'  # db_table
	fields_list = ['id', 'guid', 'application_id', 'layout_xml', 'logic_xml', 'name']
	guid_key = 'guid'  # will generate uuid automatically when created new row
	to_json_fields = ['guid', 'name']

	@cached_property
	def application(self):
		return Application.get(guid=self.application_id) if self.application_id else None

	@cached_property
	def roles(self):
		return Role.filter(workspace_id=self.application.workspace_id)

	@cached_property
	def rights(self):
		return Right.filter(workspace_id=self.application.workspace_id)

	@cached_property
	def xml_layout(self):
		return ET.fromstring(self.layout_xml or "")

	def __get_parents_path(self, node):
		result = []

		while True:
			if not node:
				break
			result = [node.attrib.get("name")] + result
			node = node.getparent()

		return result

	def get_vdomxml(self):
		vdomxml = ET.fromstring(self.xml_layout.find("VDOMXML").text or "")
		e2vdom = json.loads(self.xml_layout.find("E2VDOM").text or "{}")

		for w_xml in list(vdomxml.iter("WIDGET")):
			w_guid = w_xml.get("guid")
			w = Widget.get(guid=w_guid)

			w_vdomxml = w.get_vdomxml()
			w_prefix = self.__get_parents_path(w_xml.getparent())
			e2vdom.update(w.get_e2vdom(w_prefix))

			w_xml.clear()
			w_xml.tag = w_vdomxml.tag
			for k, v in w_vdomxml.attrib.items():
				w_xml.attrib[k] = v

			for x in w_vdomxml:
				w_xml.append(x)

		return ET.tostring(vdomxml), json.dumps(e2vdom)

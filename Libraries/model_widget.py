"""
	Widget model
"""
import json
import base64
import lxml.etree as ET
from copy import copy

from utils_base_classes import SoftDeletionModel, cached_property
from model_workspace import Workspace


WIDGET_XML_TEMPLATE = u"""
<WIDGET name="">
  <VDOMXML><![CDATA[]]>
  </VDOMXML>
  <E2VDOM></E2VDOM>
</WIDGET>
"""


class Widget(SoftDeletionModel):

	db_table = 'eapp_widget'  # db_table
	fields_list = ['id', 'guid', 'workspace_id', 'source', 'name']
	guid_key = 'guid'  # will generate uuid automatically when created new row

	to_json_fields = ['guid', 'name']

	def __init__(self, **predefined_fields):
		super(Widget, self).__init__(**predefined_fields)
		if not self.source:
			self.source = WIDGET_XML_TEMPLATE

		self.__xml = None

	def __str__(self):
		return '%(name)s (%(id)s)%(deleted)s' % {
			'name': self.name,
			'id': self.id,
			'deleted': '[X]' if self.is_deleted else ''
		}

	@property
	def xml(self):
		if not self.__xml:
			self.__xml = ET.fromstring(self.source or "")
		return self.__xml

	def get_xml(self):
		return ET.fromstring(self.source or "")

	def set_xml(self, xml_value):
		self.source = ET.tostring(xml_value)

#	@property
#	def name(self):
#		try:
#			widget_name = self.xml.attrib.get("name")
#		except:
#			widget_name = 'widget_{}'.format(self.id)
#		return widget_name
#
#	@name.setter
#	def name(self, value):
#		try:
#			xml = self.get_xml()
#			xml.set("name", value)
#			self.set_xml(xml)
#			raise Exception(self.source)
#		except Exception, e:
#			raise Exception(str(e))

	@property
	def workspace(self):
		return Workspace.get(guid=self.workspace_id) if self.workspace_id else None

	@property
	def b64source(self):
		return base64.b64encode(self.source)

	def save(self, b64source=None):
		if b64source:
			self.source = base64.b64decode(b64source)

		super(Widget, self).save()

	def get_vdomxml(self):
		try:
			vdomxml = ET.fromstring(self.xml.find("VDOMXML").text or "")
		except:
			vdomxml = None
		return vdomxml

	def get_e2vdom(self, prefix_list=[]):
		try:

			e2 = json.loads(self.xml.find("E2VDOM").text or "{}")

			if not e2:
				return {}

			if not prefix_list:
				return e2

			e2upd = {}
			prefix = ".".join(prefix_list) + "."

			for event, actions in e2.iteritems():

				for act in actions:
					if isinstance(act, list) and ":" in act[0]:
						act[0] = prefix + act[0]

				e2upd[prefix+event] = actions

			e2 = e2upd
		except:
#			raise Exception(e)
			e2 = None
		return e2



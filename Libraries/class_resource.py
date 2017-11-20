import base64

class Resource:
	def __init__(self, res_name, res_source):
		self.name 			= res_name
		self.res_source 	= res_source

	def get_xmlnode(self):
		from class_xml_resource import XMLResource
		import base64
		xml = XMLResource()
		xml.name 			= self.name
		xml.res_source 		= base64.b64encode(self.res_source.read())

		return xml

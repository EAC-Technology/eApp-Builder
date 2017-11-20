if self.data:
	import json
	data = self.data
	d = json.loads(str(data))

	self.obj_title.value = d['name']
	self.hpt_description.htmlcode = d['description']
	self.btn_open.link = d['link']
	self.form1.link.value = d['link']
	self.btn_delete.link = d['id']


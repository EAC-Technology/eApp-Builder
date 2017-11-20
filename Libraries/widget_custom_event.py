import json
import localization

class WidgetCustomEvent:
	def __init__(self):
		self.__datatable = None
		self.__custom_event_list = None

	def set_data(self, data):
		custom_event = []
		for ce in data:
			custom_event.append({"id" : ce.id,
					"Picture" : "<img src='/e574b9ce-9582-4962-ad7b-b11820dacc3d.png' />",
					"Name" : "<h1>" + ce.name + "</h1><p></p>",
					"Edit" : "<a href=''><img src='/bfd88533-b697-4ce2-8a4f-ba85e269820b.res'/>Edit custom event</a>",
					"Delete" : "<a href=''>Delete</a>"})
		self.__custom_event_list = json.dumps(custom_event)

	def render(self, datatable):
		self.__datatable = datatable
		self.__datatable.data = self.__custom_event_list


import managers

class License( object ):
	def get_confirmed(self):
		object = managers.xml_manager.search_object(application.id, "c09b5edd-d24b-45e5-8543-96c1c9fbbf36")
		return bool(object.attributes.value)


	def set_confirmed(self, value):
		object = managers.xml_manager.search_object(application.id, "c09b5edd-d24b-45e5-8543-96c1c9fbbf36")
		object.set_attributes({"value": unicode(value)})


	confirmed = property(get_confirmed, set_confirmed)

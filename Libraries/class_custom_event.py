from class_db import Database
from VEE_core import engine
from utils.uuid import uuid4

class CustomEvent:
	def __init__(self):
		self.id 			= None
		self.name 			= None
		self.guid	 		= None
		self.plugin_guid	= None


	def __fill_from_row(self, row):
		self.id 			= row[0]
		self.name 			= row[1]
		self.guid	 		= row[2]
		self.plugin_guid	= row[3]

		return self

	@classmethod
	def get_by_id(self, id):
		db_row = Database.macrosdb().fetch_one(	"""
			SELECT
				custom_event.id,
				custom_event.name,
				custom_event.guid,
				custom_event.plugin_guid
			FROM `custom_event`
			WHERE custom_event.id=?""", (id, ))

		return self().__fill_from_row(db_row) if db_row else None

	@classmethod
	def register_custom_event_by_guid( self, guid ):
		custom_event = self.get_custom_event_by_guid( guid )
		if custom_event: custom_event.register()


	def __internal_name( self ):
		return "{0}:{1}".format( self.plugin_guid, self.name ).encode( "utf-8" ).lower()


	def register( self ):
		pass
		#engine.add_timer( self.__internal_name(), self.period, self.guid )

	def unregister( self ):
		pass
		#engine.delete_timer( self.__internal_name() )

	def update_custom_event( self ):
		pass
		#engine.update_timer( self.__internal_name(), self.period, self.guid )


	@classmethod
	def get_custom_event_by_plugin_guid(self, plugin_guid):
		db_rows = Database.macrosdb().fetch_all(	"""
			SELECT
				custom_event.id,
				custom_event.name,
				custom_event.guid,
				custom_event.plugin_guid
			FROM `custom_event`
			WHERE custom_event.plugin_guid=?""", (plugin_guid, ) )
		return [self().__fill_from_row(row) for row in db_rows]

	@classmethod
	def get_custom_event_by_guid(self, guid):
		db_row = Database.macrosdb().fetch_one(	"""
			SELECT
				custom_event.id,
				custom_event.name,
				custom_event.guid,
				custom_event.plugin_guid
			FROM `custom_event`
			WHERE custom_event.guid=?""", (guid, ))

		return self().__fill_from_row(db_row) if db_row else None


	def save(self):
		return self.__update() if self.id else self.__insert()

	def __insert(self):
		self.guid = str(uuid4()) if self.guid is None else self.guid
		#raise Exception(self.guid, self.name)
		self.id = Database.macrosdb().commit(
			"""INSERT INTO custom_event (name, guid, plugin_guid) VALUES (?,?,?)""",
			 (self.name, self.guid, self.plugin_guid ) )

		self.register()
		return self

	def __update(self):
		Database.macrosdb().commit(
			"""UPDATE custom_event
				SET
					name=?,
					guid=?,
					plugin_guid=?
					WHERE id=?""",
			 (self.name, self.guid, self.plugin_guid, self.id))
		self.update_custom_event()
		return self

	def delete(self):
		from class_macro import Macros

		macros_list = Macros.get_macros_by_custom_event_guid(self.guid)
		for macros in macros_list:
			macros.class_name = "NULL"
			macros.custom_event = "NULL"
			macros.is_button_macros = "1"
			macros.on_board = "0"
			macros.save()

		self.unregister()
		Database.macrosdb().commit("""DELETE FROM custom_event WHERE id=?""", (self.id,))


	def get_xmlnode(self):
		from class_xml_custom_event import XMLCustomEvent
		import base64
		xml = XMLCustomEvent()
		xml.name 			= self.name
		xml.guid 			= self.guid

		return xml

	def generate_xml(self):
		return self.get_xmlnode().toprettyxml().encode("utf8")

	def fill_from_xml(self, xml, plugin_guid):
		self.name 				= xml.name
		self.guid	 			= xml.guid
		self.plugin_guid		= plugin_guid
		self.save()

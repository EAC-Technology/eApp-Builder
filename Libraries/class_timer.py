from class_db import Database
from VEE_core import engine
from utils.uuid import uuid4

class Timer:
	def __init__(self):
		self.id 			= None
		self.name 			= None
		self.period 		= None
		self.guid	 		= None
		self.plugin_guid	= None


	def __fill_from_row(self, row):
		self.id 			= row[0]
		self.name 			= row[1]
		self.period		 	= row[2]
		self.guid	 		= row[3]
		self.plugin_guid	= row[4]

		return self

	@classmethod
	def get_by_id(self, id):
		db_row = Database.macrosdb().fetch_one(	"""
			SELECT
				timer.id,
				timer.name,
				timer.period,
				timer.guid,
				timer.plugin_guid
			FROM `timer`
			WHERE timer.id=?""", (id, ))

		return self().__fill_from_row(db_row) if db_row else None

	@classmethod
	def register_timer_by_guid( self, guid ):
		timer = self.get_timer_by_guid( guid )
		if timer: timer.register()


	def __internal_name( self ):
		return "{0}:{1}".format( self.plugin_guid, self.name ).encode( "utf-8" ).lower()


	def register( self ):
		engine.add_timer( self.__internal_name(), self.period, self.guid )

	def unregister( self ):
		engine.delete_timer( self.__internal_name() )

	def update_timer( self ):
		engine.update_timer( self.__internal_name(), self.period, self.guid )


	@classmethod
	def get_timer_by_plugin_guid(self, plugin_guid):
		db_rows = Database.macrosdb().fetch_all(	"""
			SELECT
				timer.id,
				timer.name,
				timer.period,
				timer.guid,
				timer.plugin_guid
			FROM `timer`
			WHERE timer.plugin_guid=?""", (plugin_guid, ) )
		return [self().__fill_from_row(row) for row in db_rows]

	@classmethod
	def get_timer_by_guid(self, guid):
		db_row = Database.macrosdb().fetch_one(	"""
			SELECT
				timer.id,
				timer.name,
				timer.period,
				timer.guid,
				timer.plugin_guid
			FROM `timer`
			WHERE timer.guid=?""", (guid, ))

		return self().__fill_from_row(db_row) if db_row else None


	def save(self):
		return self.__update() if self.id else self.__insert()

	def __insert(self):
		self.guid = str(uuid4()) if self.guid is None else self.guid
		self.id = Database.macrosdb().commit(
			"""INSERT INTO timer (name, period, guid, plugin_guid) VALUES (?,?,?,?)""",
			 (self.name, self.period, self.guid, self.plugin_guid ) )

		self.register()
		return self

	def __update(self):
		Database.macrosdb().commit(
			"""UPDATE timer
				SET
					name=?,
					period=?,
					guid=?,
					plugin_guid=?
					WHERE id=?""",
			 (self.name, self.period, self.guid, self.plugin_guid, self.id))
		self.update_timer()
		return self

	def delete(self):
		from class_macro import Macros

		macros_list = Macros.get_macros_by_timer_guid(self.guid)
		for macros in macros_list:
			macros.class_name = "NULL"
			macros.timer_guid = "NULL"
			macros.is_button_macros = "1"
			macros.on_board = "0"
			macros.save()

		self.unregister()
		Database.macrosdb().commit("""DELETE FROM timer WHERE id=?""", (self.id,))


	def get_xmlnode(self):
		from class_xml_timer import XMLTimer
		import base64
		xml = XMLTimer()
		xml.name 			= self.name
		xml.guid 			= self.guid
		xml.period 			= self.period

		return xml

	def generate_xml(self):
		return self.get_xmlnode().toprettyxml().encode("utf8")

	def fill_from_xml(self, xml, plugin_guid):
		self.name 				= xml.name
		self.guid	 			= xml.guid
		self.period				= xml.period
		self.plugin_guid		= plugin_guid
		self.save()

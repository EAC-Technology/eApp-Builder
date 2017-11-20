from class_db import Database
from utils.uuid import uuid4
import base64

class Plugins:
	def __init__(self):
		self.id 			= None
		self.name 			= None
		self.description 	= None
		self.author 		= None
		self.picture 		= None
		self.guid 			= None
		self.zindex			= None
		self.version		= None
		self.protected		= None
		self.__macros		= []
		self.__timer		= []
		self.__custom_event = []


	def __fill_from_row(self, row):
		self.id 			= row[0]
		self.name 			= row[1]
		self.description 	= row[2]
		self.author 		= row[3]
		self.picture 		= row[4]
		self.guid	 		= row[5]
		self.zindex	 		= row[6]
		self.version 		= row[7]
		self.protected 		= row[8]

		return self


	@classmethod
	def get_all(self):
		db_rows = Database.macrosdb().fetch_all(	"""
			SELECT
				plugin.id,
				plugin.name,
				plugin.description,
				plugin.author,
				plugin.picture,
				plugin.guid,
				plugin.zindex,
				plugin.version,
				plugin.protected
			FROM `plugin`""", )

		return [self().__fill_from_row(row) for row in db_rows]

	def get_macros(self):
		from class_macro import Macros
		self.__macros = Macros.get_macros_by_plugin_guid(self.guid)
		return self.__macros

	def get_timer(self):
		from class_timer import Timer
		self.__timer = Timer.get_timer_by_plugin_guid(self.guid)
		return self.__timer

	def get_custom_event(self):
		from class_custom_event import CustomEvent
		self.__custom_event = CustomEvent.get_custom_event_by_plugin_guid(self.guid)
		return self.__custom_event

	@classmethod
	def get_by_id(self, id):
		db_row = Database.macrosdb().fetch_one(	"""
			SELECT
				plugin.id,
				plugin.name,
				plugin.description,
				plugin.author,
				plugin.picture,
				plugin.guid,
				plugin.zindex,
				plugin.version,
				plugin.protected
			FROM `plugin`
			WHERE id=?""", (id,))

		return self().__fill_from_row(db_row) if db_row else None

	@classmethod
	def get_by_guid(self, guid):
		db_row = Database.macrosdb().fetch_one(	"""
			SELECT
				plugin.id,
				plugin.name,
				plugin.description,
				plugin.author,
				plugin.picture,
				plugin.guid,
				plugin.zindex,
				plugin.version,
				plugin.protected
			FROM `plugin`
			WHERE guid=?""", (guid,))

		return self().__fill_from_row(db_row) if db_row else None


	def save(self):
		return self.__update() if self.id else self.__insert()

	def __insert(self):
		self.id = Database.macrosdb().commit(
			"""INSERT INTO plugin (name, description, author, picture, guid, zindex, version, protected) VALUES (?,?,?,?,?,?,?,?)""",
			 (self.name, self.description, self.author, self.picture, self.guid, self.zindex, self.version, self.protected))
		return self

	def __update(self):
		Database.macrosdb().commit(
		"""UPDATE plugin
			SET
				name=?,
				description=?,
				author=?,
				picture=?,
				guid=?,
				zindex=?,
				version=?,
				protected=?
			WHERE id=?""",
		 (self.name, self.description, self.author, self.picture, self.guid, self.zindex, self.version, self.protected, self.id))

		return self

	def delete(self,keep_storage=False):
		macros_list = self.get_macros()
		for macro in macros_list:
			macro.delete()
		timer_list = self.get_timer()
		for timer in timer_list:
			timer.delete()
		custom_event_list = self.get_custom_event()
		for cevent in custom_event_list:
			cevent.delete()

		Database.macrosdb().commit("""DELETE FROM plugin WHERE id=?""", (self.id,))
		if not keep_storage:
			Database.macrosdb().commit("""DELETE FROM kv_macro_storage WHERE namespace=?""", (self.guid,))

	def export(self):
		from StringIO import StringIO
		import base64

		from class_xml_plugin import XMLPlugin
		xml_plugin = XMLPlugin()

		xml_plugin.picture = base64.b64encode(application.storage.readall(self.picture)) if self.picture else ''
		xml_plugin.description = self.description if self.description else ''
		xml_plugin.name = self.name if self.name else ''
		xml_plugin.version = self.version if self.version else ''
		xml_plugin.author = self.author if self.author else ''
		xml_plugin.guid = self.guid


		#raise Exception(name, description, author)
		#outp.write(xml_plugin"<plugin guid='" + self.guid + "' name='" + name + "' description='" + description + "' picture='" + picture + "' author='" + author + "' version='"+ version +"'>")

		timers = self.get_timer()
		for timer in timers:
			from class_timer import Timer
			t = Timer.get_by_id(timer.id)
			xml_plugin.append_child( t.get_xmlnode() )

		custom_events = self.get_custom_event()
		for cevent in custom_events:
			from class_custom_event import CustomEvent
			ce = CustomEvent.get_by_id(cevent.id)
			xml_plugin.append_child( ce.get_xmlnode() )

		from VEE_sqlite3 import DatabaseManager
		from VEE_resources import ResourceFolderManager

		db_list = DatabaseManager(self.guid).databaselist
		for db in db_list:
			from class_plugin_db import PluginDB
			plugin_db = PluginDB(db, DatabaseManager(self.guid).export_db(db))
			xml_plugin.append_child( plugin_db.get_xmlnode() )

		res_list = ResourceFolderManager(self.guid).resourcelist
		for res in res_list:
			from class_resource import Resource
			resource = Resource(res, ResourceFolderManager(self.guid).export_res(res))
			xml_plugin.append_child( resource.get_xmlnode() )

		macros = self.get_macros()
		for macro in macros:
			from class_macro import Macros
			m = Macros.get_by_id(macro.id)
			xml_plugin.append_child( m.get_xmlnode() )

		outp = StringIO()
		outp.write( xml_plugin.toprettyxml().encode( 'utf8' ) )
		return outp

	def fill_from_xml(self, xml):
		self.name = xml.name
		self.description = xml.description
		self.guid = xml.guid
		self.version = xml.version
		self.author = xml.author
		self.protected = xml.protected

		plugin_picture_name = ""
		self.picture = ""
		if xml.picture:
			self.picture = plugin_picture_name = str(uuid4())
			application.storage.write(plugin_picture_name, base64.b64decode(xml.picture))
		self.save()

	def get_md5(self):
		import md5
		return md5.md5(self.export().getvalue()).hexdigest()

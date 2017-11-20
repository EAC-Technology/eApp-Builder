"""
Description:
	Interface for automaticly database updating

Parameters:

Obsolete:

Usage:
"""

from class_db import Database
from datetime import datetime
import ProAdmin


class Update( object ):

	dbtable_guid 	= "92269b6e-4b6b-4882-852f-f7ef0e89c079" # dbtable type id
	dbschema_guid 	= "da21b65f-6452-4c45-b1a7-984dba4e309f" # db page id
	#customdb_guid	= "3a6c8729-30e8-45cc-a146-ff2854f251f5" # customdb id

	@classmethod
	def get_current_version(self):
		query = """SELECT name FROM sqlite_master
					WHERE type='table' and name='config' """
		res = Database.maindb().fetch_one(query)
		if res:
			query = """SELECT value FROM config
					WHERE key='db_version' """
			if res:
				res = Database.maindb().fetch_one(query)
				return int(res[0])

		return 0


	@classmethod
	def set_version_value(self, ver):
		if ver > 0:
			query = """UPDATE config
						SET	value = ?
						WHERE key='db_version' """
		else:
			query = """INSERT OR REPLACE INTO config (key, value ) VALUES ('db_version',?)"""
		res = Database.maindb().commit(query,(ver,),)
		return True


	@classmethod
	def set_update(self, ver):
		pass
#		if 		ver == 1:
#			self.set_update_1()
#		elif 	ver == 2:
#			self.set_update_2()
#		elif 	ver == 3:
#			self.set_update_3()
#		elif 	ver == 4:
#			self.set_update_4()
#		elif 	ver == 5:
#			self.set_update_5()
#		elif 	ver == 6:
#			self.set_update_6()
#		elif	ver == 7:
#			self.set_update_7()
#		elif 	ver == 8:
#			self.set_update_8()
#		elif 	ver == 9:
#			self.set_update_9()

		return True


	@classmethod
	def get_max_version(self):
		return 1


	@classmethod
	def update(self):
		cur_version = self.get_current_version()
		max_version = self.get_max_version()


		if cur_version < max_version:
			#raise Exception(str(cur_version)+":"+str(max_version))
			for i in xrange(cur_version,max_version):
				self.set_update(i+1)


		return	 self.get_current_version()


	@classmethod
	def serialize_acl_tree( self, root ):
		seria = []
		for o in root.child_objects():
			seria.append({
							"type"		: o.type,
							"name"		: o.name,
							"guid"		: o.guid,
							"childs"	: self.serialize_acl_tree( o ),
							"rules"		: self.serialize_acl_rules( o )
						})
		return seria


	@classmethod
	def serialize_acl_rules( self, acl_obj ):
		return [{ "subject_guid" : r.subject.guid, "access" : r.access } for r in acl_obj.rules() ]


	@classmethod
	def apply_acl_tree( self, destination, seria ):
		for record in seria:
			obj = destination.create_child( type=record["type"], name=record["name"], guid=record["guid"] )
			self.apply_acl_rules( obj, record["rules"] )
			obj.save()
			self.apply_acl_tree( obj, record["childs"] )


	@classmethod
	def apply_acl_rules( self, destination, seria ):
		for rec in seria:
			destination.add_rule( ProAdmin.application().get_subject( guid=rec["subject_guid"] ), access=rec["access"] )


	@classmethod
	def set_table(self, table_name, custom_id=None):
		import xml

		application = xml.xml_manager.get_application(application.id)
		parent = application.search_object(Update.dbschema_guid if not custom_id else custom_id)

		#raise Exception(str(parent.get_objects_by_name().keys()))
		if table_name in parent.get_objects_by_name().keys():
			pass
		else:
			obj_name,obj_id = application.create_object(Update.dbtable_guid, parent)
			obj = application.search_object(obj_id)
			obj.set_name(table_name)
			obj.set_attributes({"top":500,"left":600,"width": 200,"height":300})

			import managers
			managers.DatabaseManager.get_database(application.id, Update.dbschema_guid if not custom_id else custom_id).tables_index[obj_id] = table_name
			managers.DatabaseManager.save_index()

			#raise Exception("Done")

		return True

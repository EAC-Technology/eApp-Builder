"""
	Classes to be used for inheritance in other classes/models
"""

from class_db import Database
from utils.uuid import uuid4
from collections import OrderedDict, defaultdict
from app_settings import settings
import json
from cgi import escape as escape_html


class cached_property(object):

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls=None):
        result = instance.__dict__[self.func.__name__] = self.func(instance)
        return result


class DB_model(object):
	"""
		Database class to automatically wrap basic and common requests
	"""

	DBMAIN = Database.maindb
	DBMACRO = Database.macrosdb

	STATEMENT_SELECT = 'select'
	STATEMENT_DELETE = 'delete'
	STATEMENT_INSERT = 'insert'
	STATEMENT_UPDATE = 'update'
	cached = cached_property

	database = DBMAIN  # db link
	db_table = ''  # db_table

	fields_list = ['id']  # All database fields to be processed
	primary_key = 'id'  # will be used for row update (must be in fields_list too)
	guid_key = ''  # will generate uuid automatically when created new row
	json_fields = {}  # will treat as json (dict) fields - work as dict and saved as json
	to_json_fields = fields_list  # will add this object attrs as json for to_json method
	to_json_childs = []  # will add this object foreign objects as json for to_json method

	def __init__(self, **predefined_fields):
		""" provide initial data through predefined_fields (keys must be in fields_list)
		"""

		self.errors = defaultdict(list)

		for field in self.fields_list:
			if field in self.json_fields:
				setattr(self, field, predefined_fields.get(field, {}))
			else:
				setattr(self, field, predefined_fields.get(field, None))

		# fields without primary key, commonly used in the class
		self._fields_without_primary_key = [field for field in self.fields_list if field != self.primary_key]

	def __str__(self):
		# if object has 'name' attr (commonly used), take it, otherwise - class name
		name = self.name if 'name' in self.fields_list else self.__class__.__name__

		return u'%(name)s (%(id)s)' % {
			'name': name,
			'id': self.id,
		}

	def __fill_from_row(self, row):
		assert len(row) == len(self.fields_list),\
			'''Incorrect database table list: {}, and model '{}' fields_list: {}'''.format(
				str(row.keys()), self.__class__.__name__, str(self.fields_list)
			)

		for index, field in enumerate(self.fields_list):
			setattr(self, field, row[index])

		for json_field in self.json_fields:
			json_value = getattr(self, json_field, None)
			json_value = {} if not json_value else json.loads(json_value)
			setattr(self, json_field, json_value)

		return self

	@classmethod
	def __validate_class(cls):
		assert cls.database
		assert cls.primary_key
		assert cls.primary_key in cls.fields_list

	@classmethod
	def __validate_keys(cls, keys):
		for key in keys:
			if key not in cls.fields_list:
				raise Exception('Field \'{}\' is not defined in {} model fields list. Valid are: {}'.format(
					key, cls.__name__, cls.fields_list
				))

	@classmethod
	def _sql_request(cls, statement=STATEMENT_SELECT, instance=None, filter={}):
		""" Common method to form sql query and parameters for it to be passed.
			By default, it will return ALL objects of this model.

			For SELECT statement use 'filter' keyword to provide arguments for WHERE clause, omit to get ALL objects.
		"""
		cls.__validate_class()
		query = ''
		params = []

		# by default, SELECT is used
		if statement == cls.STATEMENT_SELECT:
			where_clause = ''

			if filter:

				# validate model field names
				filter_args = OrderedDict(filter)
				cls.__validate_keys(filter_args.keys())

				# form WHERE clause and values to be provided through database fetch method
				where_clause = 'WHERE {}'.format(
					' AND '.join(
						['{}=?'.format(field_key) for field_key in filter_args.keys()]
					)
				)

				params = [field_value for field_value in filter_args.values()]

			fields_list_all = ', '.join([
				'{model_name}.{field_name}'.format(
					model_name=cls.db_table,
					field_name=field_name,
				) for field_name in cls.fields_list
			])

			query = "SELECT {field_names} FROM `{db_table}` {where_clause}".format(
				field_names=fields_list_all,
				db_table=cls.db_table,
				where_clause=where_clause
			)
		else:
			# for other statements instance must be provided
			assert isinstance(instance, cls), 'Provide instance of the same cls'

			if statement == cls.STATEMENT_INSERT:

				fields_list = ', '.join(instance._fields_without_primary_key)
				fields_question_marks = ', '.join('?' for arg in instance._fields_without_primary_key)

				query = "INSERT INTO `{db_table}` ({fields_list}) VALUES ({fields_question_marks})".format(
					db_table=cls.db_table,
					fields_list=fields_list,
					fields_question_marks=fields_question_marks
				)
				instance.json_pack()
				params = [getattr(instance, field, '') for field in instance._fields_without_primary_key]

			elif statement == cls.STATEMENT_UPDATE:

				update_fields = ', '.join([
					'{}=?'.format(field) for field in instance._fields_without_primary_key
				])

				query = "UPDATE `{db_table}` SET {update_fields} WHERE id=?".format(
					db_table=cls.db_table,
					update_fields=update_fields
				)

				instance.json_pack()
				params = [getattr(instance, field, '') for field in instance._fields_without_primary_key]
				params.append(getattr(instance, cls.primary_key, 0))

			elif statement == cls.STATEMENT_DELETE:
				query = "DELETE FROM `{}` WHERE id=?".format(cls.db_table)
				instance.json_pack()
				params = [getattr(instance, cls.primary_key, 0)]

		return query, params

	@classmethod
	def all(cls):
		""" Returns all instances in database of current model """

		db_rows = cls.database().fetch_all(
			*cls._sql_request()
		)

		return [cls().__fill_from_row(row) for row in db_rows]

	@classmethod
	def get(cls, **kwargs):
		""" Return only one object of this instance.
			Return None if object not found and raise Exception if multiple objects found.
		"""
		if len(kwargs) is 0:
			raise Exception('Provide at least one argument for get/filter lookup')
		db_row = cls.database().fetch_one(
			*cls._sql_request(filter=kwargs)
		)

		return cls().__fill_from_row(db_row) if db_row else None

	@classmethod
	def filter(cls, **kwargs):
		""" Return a list of objects found with this arguments """

		if len(kwargs) is 0:
			raise Exception('Provide at least one argument for get/filter lookup')

		db_rows = cls.database().fetch_all(
			*cls._sql_request(filter=kwargs)
		)

		return [cls().__fill_from_row(row) for row in db_rows]

	def save(self):
		""" Use save() method to define when instance need to be inserted or updated """
		return self.__update() if getattr(self, self.primary_key, 0) else self.__insert()

	def __insert(self):
		""" Creates valid INSERT sql query """

		if self.guid_key and self.guid_key in self.fields_list:
			setattr(self, self.guid_key, str(uuid4()))

		primary_key_db = self.database().commit(
			*self._sql_request(statement=self.STATEMENT_INSERT, instance=self)
		)

		setattr(self, self.primary_key, primary_key_db)
		return self

	def __update(self):
		""" Creates valid UDPATE sql query """

		self.database().commit(
			*self._sql_request(statement=self.STATEMENT_UPDATE, instance=self)
		)

		return self

	def delete(self):
		""" Creates valid DELETE sql query """
		self.database().commit(
			*self._sql_request(statement=self.STATEMENT_DELETE, instance=self)
		)

	def json_pack(self):
		for json_field in self.json_fields:
			setattr(self, json_field,
				json.dumps(getattr(self, json_field, {}))
			)

	def reload(self):
		""" Refresh instance from database like refresh_from_db() method """
		assert getattr(self, self.primary_key), 'You need to save the instance first in order to reload it'
		db_row = self.database().fetch_one(
			*self._sql_request(filter={self.primary_key: getattr(self, self.primary_key)})
		)
		if db_row:
			self.__fill_from_row(db_row)

	def to_json(self, include=[]):
		""" Convert instance to JSON format according with to_json_fields and to_json_childs fields """

		result_json = {}
		for field in self.to_json_fields + include:
			result_json[field] = getattr(self, field, "NONE")

		for child_field in self.to_json_childs:
			result_json[child_field] = []
			childs_list = getattr(self, child_field, [])
#			raise Exception(child_field + " " +str(childs_list))

			for child_instance in childs_list:
				if hasattr(child_instance, "to_json"):
					result_json[child_field].append( child_instance.to_json() )

		return result_json

	def fill_from_json(self, json_data):
		""" Get field values from json (dict) and apply all to model """

		for field in json_data:
			if field in self.fields_list:
				setattr(self, field, json_data[field])


class SoftDeletionModel(DB_model):
	"""
		You can activate soft_deletion feature.
		To work properly, you have to add 'deleted' field in database table.
		and you can use different name for it in is_deleted_field.
		use INCLUDE_DELETED_KEY=True in filter lookups to add previously deleted objects if needed
	"""
	INCLUDE_DELETED_KEY = 'include_deleted'  # add this key for lookups to return all objects including deleted
	is_deleted_field = 'deleted'  # will be used as boolean field if soft_deletion == True
	soft_deletion = settings.SOFT_DELETE  # set False to force deletion of db rows.

	def __init__(self, **predefined_fields):
		super(SoftDeletionModel, self).__init__(**predefined_fields)
		setattr(self, self.is_deleted_field, '0')
		self._fields_without_primary_key.append(self.is_deleted_field)

	@classmethod
	def _sql_request(cls, **kwargs):
		if cls.is_deleted_field not in cls.fields_list:
			cls.fields_list.append(cls.is_deleted_field)

		if kwargs.get('statement', cls.STATEMENT_SELECT) == cls.STATEMENT_SELECT:
			filter = kwargs.get('filter', {})
			include_deleted = filter.pop(cls.INCLUDE_DELETED_KEY, False)

			# add soft_deletion key if not manually added
			if cls.soft_deletion and cls.is_deleted_field not in filter and not include_deleted:
				filter[cls.is_deleted_field] = '0'
			kwargs['filter'] = filter
		return super(SoftDeletionModel, cls)._sql_request(**kwargs)

	@property
	def is_deleted(self):
		""" Soft deletion property field"""
		return getattr(self, self.is_deleted_field, '0') != '0'

	def delete(self):
		""" Mark instance as deleted unless soft_deletion is not turned off, otherwise default delete from db """
		if self.soft_deletion:
			setattr(self, self.is_deleted_field, '1')
			self.save()
		else:
			super(SoftDeletionModel, self).delete()


class TemplateCollection:
	"""
		Allows to create html renders from provided objects by using specific
		template, collection and new_object_template.
	"""

	template = u'' 	# html template for single object
	collection = u'<div class="row">{objects}</div>' # html template for collection of objects
	new_object_template = ''  # last object to be rendered as "create new"
	serializable = False  # if need to render json
	is_html = True   # if need to render html
	escape_list = []  # escape tags

	def __init__(self, objects=None, many=True, add_new=False, selected_id=[]):
		""" Use 'many' argument so instance will generate a collection of renders """

		self.many = many
		self.objects = objects
		self.add_new = add_new
		self.selected_id = selected_id

		self.html = ''
		self.json = {}

		if self.objects is not None:
			if self.is_html:
				self.render()

			if self.serializable:
				self.serialize()

	def __unicode__(self):
		return u"{classname}: [{objects}]".format(
			classname=self.__class__.__name__,
			objects=u', '.join([unicode(obj) for obj in self.objects ])
		)

	def context(self, object):
		""" context to be applied to html template """
		return {}

	def context_json(self, object):
		""" By default, return same result as context, override to use your own params """
		return self.context(object)

	def escape_context(self, context):
		for escape_field in self.escape_list:
			context[escape_field] = escape_html(context[escape_field]) if context[escape_field] else ""
		return context

	def render(self):
		if self.many:
			context = {}
			context['objects'] = u''.join([self.template.format(
				**self.escape_context(self.context(object))
			) for object in self.objects])

			if self.add_new:
				context['objects'] = context.get('objects', '') + self.new_object_template

			self.html = self.collection.format(**context)
		else:
			context = self.escape_context(self.context(self.objects))
			self.html = self.template.format(**context)

		return self

	def serialize(self):
		self.json = {}
		if self.many:
			for index, object in enumerate(self.objects):
				self.json[index] = json.dumps(self.escape_context(self.context_json(object)))
			self.json = json.dumps(self.json)
		else:
			context = self.escape_context(self.context_json(self.objects))
			self.json = json.dumps(context)

		return self


class ModelForm(object):

	model = object  # should be an object with fields_list attribute
	exclude = ['id', 'guid']  # will exclude values from kwargs if provided
	mandatory = []  # this fields must be non-empty
	fields_list = []  # if non empty, then model fields_list is used

	def __init__(self, instance=None, instance_id=None, **kwargs):
		self.fields = {}
		self.errors = defaultdict(list)

		if instance is None:
			self.instance = self.model.get(**{self.model.primary_key: instance_id}) if instance_id else self.model()
		else:
			assert isinstance(instance, self.model)
			self.instance = instance

		if not self.fields_list:
			self.fields_list = self.model.fields_list

		self.set_data(**kwargs)

	def set_data(self, **kwargs):
		for key in kwargs:
			if key not in self.fields_list:
				raise Exception('Incorrect input field name "{}", check model fields_list'.format(key))

			if key in self.exclude:
				continue

			self.fields[key] = kwargs[key]

	def clean(self):
		self.errors = defaultdict(list)
		for key in self.mandatory:
			if not self.fields[key]:
				self.errors[key].append('Must not be empty')

	def is_valid(self):
		self.clean()
		return False if self.errors else True

	def save(self):
		for field_name in self.fields:
			setattr(self.instance, field_name, self.fields[field_name])

		self.instance.save()

	def delete(self):
		if self.instance and self.instance.id:
			self.instance.delete()

from models import DataSource, Workspace

if 'workspace_id' not in request.arguments:
	raise Exception('Workspace ID is not provided')

workspace_id = request.arguments.get('workspace_id')
command = request.arguments.get('command', u'')

workspace = Workspace.get(guid=workspace_id)

if not workspace:
	self.action('goTo', ['/main'])

elif command in ['delete', 'update']:

	if 'data_source_id' not in request.arguments:
		raise Exception(u'DataSource ID is not provided')
	data_source_id = request.arguments['data_source_id']
	data_source = DataSource.get(guid=data_source_id, workspace_id=workspace.guid)

	if data_source:
		if command == 'delete':
			data_source.delete()
		else:
			connector = request.arguments['connector']
			if connector:
				data_source.connector = connector
				data_source.save()

	self.dialog_update.action('hide', ['0'])

elif command == 'create':
	connector = request.arguments['connector']
	if connector:
		data_source = DataSource()
		data_source.workspace_id = workspace.guid
		data_source.connector = connector
		data_source.save()

"""
	Very basic url configuration
"""

WORKSPACE_HPT_CREATE = "39a22761-a03a-4cbf-b58d-f6a98f760e48"
WORKSPACE_HPT_UPDATE = "a0e87553-cf67-4f70-a2c1-3da12c4d228f"

WIDGET_HPT_CREATE = "b28ea171-b9b8-41f7-89db-cd9053951870"
WIDGET_HPT_UPDATE = "c0b69a7c-485f-43c4-bf8f-9ea65608b3bf"

DATA_SOURCE_HPT_CREATE = "dff5f5a6-6637-48c5-b724-326b8799805b"
DATA_SOURCE_HPT_UPDATE = "2d28ee72-3d64-4344-9e0d-186d5132d6da"

APPLICATION_HPT_CREATE = "650deb8d-1e1f-4508-870d-e2f2d7de6306"
APPLICATION_HPT_UPDATE = "3b7891fe-b64c-49b0-9169-3cfcdc42a2cf"

VIEW_HPT_CREATE = "e03da9a1-0428-41fb-8609-34ed98255f89"
VIEW_HPT_UPDATE = "79a712e1-9a89-42eb-b69b-8cc0d2460dc3"

ROLE_HPT_CREATE = "7145279d-fee8-4a56-bc9a-f82466047e94"
ROLE_HPT_UPDATE = "a0588c22-9acc-41e0-a5ce-f775f3c6ca92"

RESOURCE_HPT_CREATE = "bb93197a-08bc-4449-9e45-d542b5a894ad"
RESOURCE_HPT_UPDATE = "290297ae-bbb1-4b87-b071-cd1c2ef8c014"

SCRIPT_HPT_CREATE = "a5da8aa3-3f35-4c4d-88a2-76fa1532b9fc"
SCRIPT_HPT_UPDATE = "d2212f7d-22e3-4ee5-ba62-93c72bb9b86e"

ACL_HPT_UPDATE = "e5cde40e-bf9d-4c3c-a26f-203b12c3b869"

SIDEBAR_HPT_TABCHANGE = "8353196f-1eb7-4392-9e35-32e24734be53"


def reverse(url_name, **kwargs):
	assert url_name in url_conf, 'url config with "{}" name does not exists'.format(url_name)
	return url_conf[url_name].format(**kwargs)


def reverse_api_custom(container_id, api_name, **kwargs):
	return """execEventBinded('{container_id}', '{api_name}', {kwargs})""".format(
		container_id=container_id.replace('-', '_'),
		api_name=api_name,
		kwargs='{%s}' % ', '.join(["{}: '{}'".format(key, value) for key, value in kwargs.items()])
	)


def reverse_api(api_name, **kwargs):
	assert api_name in url_api_conf, 'api with "{}" name does not exists'.format(api_name)
	return reverse_api_custom(url_api_conf[api_name][0], url_api_conf[api_name][1], **kwargs)


url_conf = {
	'main': '/main',
	'workspace': '/workspace?id={workspace_id}',
	'application': '/application?id={app_id}',  # eApp application
	'widget': '/widget?id={widget_id}',  # eApp application
}


url_api_conf = {
	'workspace:create_form_show': [WORKSPACE_HPT_CREATE, 'custom'],
	'workspace:update_form_show': [WORKSPACE_HPT_UPDATE, 'custom'],
	'widget:create_form_show': [WIDGET_HPT_CREATE, 'custom'],
	'widget:update_form_show': [WIDGET_HPT_UPDATE, 'custom'],
	'data_source:create_form_show': [DATA_SOURCE_HPT_CREATE, 'custom'],
	'data_source:update_form_show': [DATA_SOURCE_HPT_UPDATE, 'custom'],
	'application:create_form_show': [APPLICATION_HPT_CREATE, 'custom'],
	'application:update_form_show': [APPLICATION_HPT_UPDATE, 'custom'],
	'application_view:tabchange': [SIDEBAR_HPT_TABCHANGE, 'custom'],
	'app_view:create_form_show': [VIEW_HPT_CREATE, 'custom'],
	'app_view:update_form_show': [VIEW_HPT_UPDATE, 'custom'],
	'app_role:create_form_show': [ROLE_HPT_CREATE, 'custom'],
	'app_role:update_form_show': [ROLE_HPT_UPDATE, 'custom'],
	'app_res:create_form_show': [RESOURCE_HPT_CREATE, 'custom'],
	'app_res:update_form_show': [RESOURCE_HPT_UPDATE, 'custom'],
	'app_acl:select_item': [ACL_HPT_UPDATE, 'custom'],
	'app_script:update_form_show': [SCRIPT_HPT_UPDATE, 'custom'],
	'app_script:create_form_show': [SCRIPT_HPT_CREATE, 'custom'],
}


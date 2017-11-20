from templates import SidebarTemplate
from urls import reverse_api

tabs = [
	dict(
		title='Structure',
#		onclick=reverse_api('application_view:tabchange', tab_name='tab_structure'),
		icon='tree-conifer',
		extra_css='disabled'
	),
	dict(
		title='View',
		onclick=reverse_api('application_view:tabchange', tab_name='tab_view'),
		icon='picture',
#		extra_css='disabled'
	),
	dict(
		title='Business Logic',
#		onclick=reverse_api('application_view:tabchange', tab_name='tab_business_logic'),
		icon='cog',
		extra_css='disabled'
	),
	dict(
		title='Parameters',
		onclick=reverse_api('application_view:tabchange', tab_name='tab_params'),
		icon='list-alt'
	),
	dict(
		title='Roles & Rights',
		onclick=reverse_api('application_view:tabchange', tab_name='tab_roles'),
		icon='user',
#		extra_css='disabled'
	),
	dict(
		title='ACL',
		onclick=reverse_api('application_view:tabchange', tab_name='tab_acl'),
		icon='lock',
#		extra_css='disabled'
	),
	dict(
		title='Resources',
		onclick=reverse_api('application_view:tabchange', tab_name='tab_resources'),
		icon='th-large',
#		extra_css='disabled'
	),
	dict(
		title='Publication',
#		onclick=reverse_api('application_view:tabchange', tab_name='tab_publication'),
		icon='save',
		extra_css='disabled'
	),
]

self.hpt_sidebar.htmlcode = SidebarTemplate(tabs, many=True).html

from utils_base_classes import TemplateCollection
from urls import reverse_api


SIDEBAR_OBJECT_HTML = u"""
	  <li class={extra_css}><a href='#' onclick="{onclick}">{icon} {title}</a></li>
"""

SIDEBAR_COLLECTION_HTML = u"""
	<ul class="nav nav-sidebar">{objects}</ul>

"""


class SidebarTemplate(TemplateCollection):
	template = SIDEBAR_OBJECT_HTML
	collection = SIDEBAR_COLLECTION_HTML

	def context(self, tab):
		icon = tab.get('icon', '')
		if icon:
			icon = u"""<span class="glyphicon glyphicon-{}" aria-hidden="true"></span>""".format(icon)
		return dict(
			title=tab.get('title', ''),
			icon=icon,
			onclick=tab.get('onclick', ''),
			extra_css=tab.get('extra_css', '')
		)


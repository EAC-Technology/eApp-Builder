
from utils_base_classes import TemplateCollection
import cgi


BREADCRUMB_OBJECT_HTML = u"""
	  <li class="{active}">{page_name}</li>
"""

BREADCRUMB_COLLECTION_HTML = u"""
	<ol class="breadcrumb" style="background-color: #ffffff !important;">{objects}</ol>
"""


class BreadcrumbTemplate(TemplateCollection):
	template = BREADCRUMB_OBJECT_HTML
	collection = BREADCRUMB_COLLECTION_HTML

	def context(self, page):
		link = page.get('link', '')
		page_name = cgi.escape(page.get('name', ''))
		if link:
			page_name = u'<a href="{}">{}</a>'.format(link, page_name)

		return dict(
			page_name=page_name,
			active='active' if page.get('is_active', False) else '',
		)


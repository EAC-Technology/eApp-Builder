import ProAdmin
from io import StringIO

REMOTE_TYPE = "RemoteApplication"

class WidgetAclObjects(object):

	def __init__(self):
		self.vdom_tree = None

		self.__app_ldap = None
		self.__app = None

	def set_app(self, app):
		self.__app = app
		self.__app_ldap = app

	def render(self, tree):
		if not tree:
			raise Exception("No TREE has been provided")

		self.vdom_tree = tree

		result_str = StringIO()
		result_str.write(u"<ul>")

		# Application node
		result_str.write( u"""
			<li id="%(guid)s" class="expanded">
				<div>
					<span class="name"><span class='acl_app_object_icon'></span>%(name)s</span>

					<!--span style="font-size:8pt;color:#555;" class="type">%(type)s</span -->
				</div>
			""" % {
				'guid'		: self.__app.guid,
				'name'		: self.__app.name,
				'type'		: "Application"
			}
			)

		result_str.write(u"<ul>")

		# objects node

#		objects = []
#		for obj in self.__app_ldap.child_objects():
#			objects.append( obj )
#			objects += self.get_childs( obj )
#
#		for obj in objects:
#			result_str.write(u"""<li id=%(guid)s>
#					<span class="name" title="%(full_name)s"><div class='acl_object_icon'>%(name)s</div></span>
#				</li>""" % {
#					'guid'	: obj.guid,
#					'name'	: obj.name if len(obj.name) < 20 else "%s..." % obj.name[:20] ,
#					'full_name' : obj.name
#				}
#			)


		for obj in self.__app_ldap.child_objects():
			result_str.write(u"""<li id=%(guid)s>
					<span class="name" title="%(full_name)s"><div class='acl_object_icon'>%(name)s</div></span>""" % {
					'guid'	: obj.guid,
					'name'	: obj.name if len(obj.name) < 20 else "%s..." % obj.name[:20] ,
					'full_name' : obj.name
				}
			)
			self.list_childs_to_str( obj, result_str )
			result_str.write(u"</li>")

		result_str.write(u"</ul></li></ul>") # objects and applications

		self.vdom_tree.data = result_str.getvalue()
		result_str.close()

	def list_childs_to_str( self, acl_obj, string ):
		string.write(u"<ul>")
		for child in acl_obj.child_objects():
			string.write(u"""<li id=%(guid)s>
					<span class="name" title="%(full_name)s"><div class='acl_object_icon'>%(name)s</div></span>
				""" % {
					'guid'	: child.guid,
					'name'	: child.name if len(child.name) < 20 else "%s..." % child.name[:20] ,
					'full_name' : child.name
				}
			)
			self.list_childs_to_str( child, string )
			string.write(u"</li>")
		string.write(u"</ul>")


	def style(self):
		return """
/* end of app_info page*/

/* Tree container */
	ul.dynatree-container
	{
		font-family: tahoma, arial, helvetica;
		font-size: 10pt; /* font size should not be too big */
		white-space: nowrap;
		padding: 3px;

		background: none;
		#border: 1px dotted gray;

		overflow: auto;

		text-align: left !important;
	}

	ul.dynatree-container ul
	{
		padding: 0 0 0 0;
		margin: 0;
	}

	ul.dynatree-container li
	{
		background: none;
		margin-left: 0;


		list-style-image: none;
		list-style-position: outside;
		list-style-type: none;
		-moz-background-clip:border;
		-moz-background-inline-policy: continuous;
		-moz-background-origin: padding;
	}
	/* Suppress lines for last child node */
	ul.dynatree-container li.dynatree-lastsib
	{
		background-image: none;
	}
	/* Suppress lines if level is fixed expanded (option minExpandLevel) */
	ul.dynatree-no-connector > li
	{
		background-image: none;
	}

	/* Style, when control is disabled */
	.ui-dynatree-disabled ul.dynatree-container
	{
		opacity: 0.5;
	/*	filter: alpha(opacity=50); /* Yields a css warning */
		background-color: silver;
	}

	/* Common icon definitions
	 */
	span.dynatree-empty,
	span.dynatree-vline,
	span.dynatree-connector,
	span.dynatree-expander,
	span.dynatree-checkbox,
	span.dynatree-radio,
	span.dynatree-drag-helper-img,
	#dynatree-drop-marker
	{
		/*background: none;*/
		padding-left: 3px;
	}

	span.dynatree-icon {
		width: 0;
		height: 16px;
	}

	/** Used by 'icon' node option: */
	ul.dynatree-container img
	{
		width: 18px;
		height: 18px;
		padding-left: 5px;
		vertical-align: top;
		border-style: none;

	}


	/* Lines and connectors
	 */

	span.dynatree-connector
	{
		/*background: none;*/
	}

	.dynatree-exp-cl span.dynatree-expander /* Collapsed, not delayed, last sibling */
	{
		background: url(/7446e209-15ac-480e-955a-d070c5129018.png) right 25% no-repeat;
	}
	.dynatree-exp-el span.dynatree-expander,  /* Expanded, not delayed, last sibling */
	.dynatree-exp-edl span.dynatree-expander  /* Expanded, delayed, last sibling */
	{
		background: url(/7446e209-15ac-480e-955a-d070c5129018.png) right 25% no-repeat;
	}


	/* Node titles */

	/* @Chrome: otherwise hit area of node titles is broken (issue 133)
	   Removed again for issue 165; (133 couldn't be reproduced) */
	span.dynatree-node
	{
	/*  display: -moz-inline-box; /* @ FF 1+2 */
	/*  display: inline-block; /* Required to make a span sizeable */
	}


	/* Remove blue color and underline from title links */
	ul.dynatree-container a
	/*, ul.dynatree-container a:visited*/
	{
		color: black; /* inherit doesn't work on IE */
		text-decoration: none;
		vertical-align: top;
		margin: 0px;
		margin-left: 3px;
	/*	outline: 0; /* @ Firefox, prevent dotted border after click */
	}

	ul.dynatree-container a:hover
	{
	/*	text-decoration: underline; */
		background: none; /* light blue */
		color: #C74551;
	}

	span.dynatree-node a
	{
		font-weight: normal;
		display: inline-block; /* Better alignment, when title contains <br> */
	/*	vertical-align: top;*/
		padding-left: 3px;
		padding-right: 3px; /* Otherwise italic font will be outside bounds */
		/*	line-height: 16px; /* should be the same as img height, in case 16 px */
		line-height: 18px;
	}
	span.dynatree-folder a
	{
		font-weight: normal;
	}


	ul.dynatree-container a:focus,
	span.dynatree-focused a:link  /* @IE */
	{
		background: none; /* gray */
	}

	span.dynatree-has-children a
	{
	}

	span.dynatree-expanded a
	{
	}

	span.dynatree-selected a
	{
		color: green;
		font-style: italic;
	}

	span.dynatree-active a
	{
		background: none!important;
		color: #C74551 !important; /* @ IE6 */

	}

	span.dynatree-active {

		display: block;
		background: url("/7f0a5366-8baa-4fa1-9ce7-42d77fd20de6.png") right center no-repeat #f2f2f2 ;
	}


	li span.dynatree-active {

	}

	/* Drag'n'drop support
	 */

	/*** Helper object */
	div.dynatree-drag-helper{}
	div.dynatree-drag-helper a
	{
		border: 1px solid gray;
		background-color: white;
		padding-left: 5px;
		padding-right: 5px;
		opacity: 0.8;
	}
	span.dynatree-drag-helper-img
	{
		/*
		position: relative;
		left: -16px;
		*/
	}
	div.dynatree-drag-helper /*.dynatree-drop-accept*/
	{
	/*    border-color: green;
		background-color: red;*/
	}
	div.dynatree-drop-accept span.dynatree-drag-helper-img
	{
		background-position: -32px -112px;
	}
	div.dynatree-drag-helper.dynatree-drop-reject
	{
		border-color: red;
	}
	div.dynatree-drop-reject span.dynatree-drag-helper-img
	{
		background-position: -16px -112px;
	}

/* end of Tree container*/
		"""

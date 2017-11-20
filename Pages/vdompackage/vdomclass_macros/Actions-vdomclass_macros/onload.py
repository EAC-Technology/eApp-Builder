import cgi
import json

parameters = json.loads(self.data)

self.text_macros_name.value = cgi.escape(parameters[ "name" ]) if parameters[ "name" ] else ""
self.image_macros.htmlcode = parameters[ "picture" ] if parameters[ "picture" ] else ""

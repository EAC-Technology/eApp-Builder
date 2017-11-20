import localization

class LocalizationRectangleWidget( object ):
	def __init__( self, page_name ):
		self.controls = {}
		self.page_name = page_name


	def add_controls( self, key, controls ):
		if type(controls) != list:
			controls = [ controls ]

		if not key in self.controls:
			self.controls[ key ] = controls
		else:
			self.controls[ key ] += controls


	def set_data( self, control_dict ):
		for key in control_dict:
			self.add_controls( key, control_dict[ key ] )


	def render( self ):
		lang = localization.get_lang_rectangle()
		lang = lang.get( self.page_name )
		if not lang: return

		for key in self.controls:
			value = lang.get( key )
			if not value: continue

			for control in self.controls[ key ]:
				control.left, control.top, control.width, control.height 	= \
				value[ 0 ], value[ 1 ], value[ 2 ], value[ 3 ]



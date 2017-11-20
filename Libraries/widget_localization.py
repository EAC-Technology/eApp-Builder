import localization

class LocalizationWidget( object ):
	def __init__( self ):
		self.controls = {}


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
		lang = localization.get_lang()

		for key in self.controls:
			value = lang.get( key )
			if not value: continue

			for control in self.controls[ key ]:
				control_attr = dir( control )

				# modify values in controls
				if   'title' in control_attr:
					control.title = value
				elif 'label' in control_attr:
					control.label = value
				elif 'text'	 in control_attr:
					control.text = value
				elif 'value' in control_attr:
					control.value = value




import ProAdmin
from class_license import License


if not License.confirmed:
	response.redirect("/license.vdom")

if not ProAdmin.scheme().is_remote():
	response.redirect( '/settings' )


from widget_localization import LocalizationWidget
localization = LocalizationWidget()
localization.add_controls( 'proadmin_attention_text', self.information_text )
localization.add_controls( 'error_response', self )
localization.render()

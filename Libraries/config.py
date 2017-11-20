proshare_config = {
	"version"			: application.itself.information_element.get_child_by_name( 'version' ).value,
	"plugin_page_dict"	: {},
	"server_type"		: "dev", #used in settings:onload
	"app_name"			: application.name #used in VScript DO NOT DELETE
}
##need for VScript STD Lib
config = proshare_config

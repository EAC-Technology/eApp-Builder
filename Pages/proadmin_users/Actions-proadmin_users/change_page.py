from widget_proadmin_users import WidgetProAdminUsers

proadmin_users_widget = WidgetProAdminUsers()
proadmin_users_widget.set_page( int(request.arguments.get("pagenumber", "1")) )
proadmin_users_widget.render(self.datatable_users, self.pager)
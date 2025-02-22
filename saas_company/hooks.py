app_name = "saas_company"
app_title = "Saas Company"
app_publisher = "Shaid Azmin"
app_description = "Saas Company"
app_email = "azmin@excelbd.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/saas_company/css/saas_company.css"
# app_include_js = "/assets/saas_company/js/saas_company.js"

# include js, css files in header of web template
# web_include_css = "/assets/saas_company/css/saas_company.css"
# web_include_js = "/assets/saas_company/js/saas_company.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "saas_company/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "saas_company.utils.jinja_methods",
# 	"filters": "saas_company.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "saas_company.add_custom_field.create_allocated_company_child_doctype"
after_install = "saas_company.add_custom_field.add_allocated_company_table_to_all_doctypes"

# after_install = "saas_company.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "saas_company.uninstall.before_uninstall"
after_uninstall = "saas_company.add_custom_field.remove_allocated_company_table_from_all_doctypes"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "saas_company.utils.before_app_install"
# after_app_install = "saas_company.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "saas_company.utils.before_app_uninstall"
# after_app_uninstall = "saas_company.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "saas_company.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
    "Newsletter": "saas_company.overrides.newsletter.SaasEmailNewsLetter.SaasEmailNewsLetter"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"*": {
		"on_update": "saas_company.add_custom_field.test",
		# "on_cancel": "method",
		# "on_trash": "method"
	},
	"User":{
		"on_update":"saas_company.add_custom_field.check_user_allocated_company"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"saas_company.tasks.all"
# 	],
# 	"daily": [
# 		"saas_company.tasks.daily"
# 	],
# 	"hourly": [
# 		"saas_company.tasks.hourly"
# 	],
# 	"weekly": [
# 		"saas_company.tasks.weekly"
# 	],
# 	"monthly": [
# 		"saas_company.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "saas_company.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "saas_company.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "saas_company.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["saas_company.utils.before_request"]
# after_request = ["saas_company.utils.after_request"]

# Job Events
# ----------
# before_job = ["saas_company.utils.before_job"]
# after_job = ["saas_company.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"saas_company.auth.validate"
# ]

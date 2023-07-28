app_name = "saudi_support"
app_title = "Saudi Support"
app_publisher = "ERPGulf"
app_description = "saudi support"
app_email = "info@ERPGulf.com"
app_license = "MIT"
fixtures = [{
		"dt": "Property Setter", "filters": [
		[
			"name", "in", [
				"Notification-channel-options",
			]
		]
	]
	}
,]

doctype_js = {
	"Notification" : "public/js/notification.js"
}

override_doctype_class = {
	"Notification": "saudi_support.overrides.notifications.ERPGulfNotification"
 }

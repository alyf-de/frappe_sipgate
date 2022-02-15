import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def after_install():
	make_custom_fields()


def make_custom_fields():
	for key, value in custom_fields.items():
		create_custom_fields({key: value}, ignore_validate=True)

	frappe.db.commit()


custom_fields = {
	"Contact": [
		{
			"fieldname": "sipgate_id",
			"fieldtype": "Data",
			"label": "Sipgate Id",
			"insert_after": "unsubscribed",
			"read_only": 1,
			"translatable": 0,
			"no_copy": 1
		}
	],
}

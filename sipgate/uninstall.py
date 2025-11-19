import frappe

from sipgate.custom_fields import get_custom_fields


def before_uninstall():
	remove_custom_fields()


def remove_custom_fields():
	print("* removing custom fields...")
	for doctype, custom_fields in get_custom_fields().items():
		for cf in custom_fields:
			frappe.db.delete(
				"Custom Field",
				{
					"dt": doctype,
					"fieldname": cf.get("fieldname"),
				},
			)

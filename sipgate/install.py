from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

from sipgate.custom_fields import get_custom_fields


def after_install():
	make_custom_fields()


def make_custom_fields() -> None:
	create_custom_fields(get_custom_fields())

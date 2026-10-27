"""Apps screen visibility for Sipgate."""

import frappe

SIPGATE_MODULE = "Sipgate"


def has_app_permission() -> bool:
	"""Return whether the session user may open Sipgate on the apps screen."""
	if frappe.session.user == "Guest":
		return False

	user = frappe.get_user()
	if not user.allow_modules:
		user.build_permissions()

	return SIPGATE_MODULE in user.allow_modules

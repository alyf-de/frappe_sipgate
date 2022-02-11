# Copyright (c) 2022, ALYF GmbH and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from typing import Union
from sipgate.sipgate_client import SipgateClient


class SipgateSettings(Document):
	pass


def sync_to_sipgate(doc=None, method=None):
	sipgate_settings = frappe.get_single("Sipgate Settings")
	if not sipgate_settings.enabled:
		return

	payload = get_payload(doc)
	sipgate = SipgateClient(
		sipgate_settings.url, sipgate_settings.token_id, sipgate_settings.token, payload
	)

	try:
		if doc.sipgate_id:
			sipgate.update()
		else:
			sipgate.upload()
			id = sipgate.get_sipgate_id(get_contact_number(doc))
			frappe.db.set_value(doc.doctype, doc.name, "sipgate_id", id)
	except Exception:
		frappe.msgprint(_("Couldn't sync contact to Sipgate."))
		frappe.log_error(frappe.get_traceback())


def get_payload(doc: object) -> frappe._dict:
	contact_dict = {
		"name": f"{doc.get('first_name', '')} {doc.get('last_name', '')}",
		"family": doc.get("last_name", ""),
		"given": doc.get("first_name", ""),
		"emails": [
			{
				"email": email.email_id,
				"type": [is_primary_email(email)],
			}
			for email in doc.email_ids
			if email
		],
		"numbers": [
			{
				"number": phone.phone,
				"type": [is_primary_phone(phone)],
			}
			for phone in doc.phone_nos
			if phone
		],
		"scope": "SHARED",
	}

	if doc.company_name:
		contact_dict.update({"organization": [[doc.company_name]]})

	if doc.get("sipgate_id"):
		contact_dict.update({"id": doc.get("sipgate_id")})

	return frappe._dict(contact_dict)


def get_contact_number(doc) -> Union[str, None]:
	return doc.phone_nos[0].phone if doc.phone_nos else None


def is_primary_phone(phone: object) -> str:
	return "primary" if phone.is_primary_mobile_no or phone.is_primary_phone else ""


def is_primary_email(email: object) -> str:
	return "primary" if email.is_primary else ""


# Copyright (c) 2022, ALYF GmbH and contributors
# For license information, please see license.txt

from typing import Optional, Union

import frappe
from frappe.model.document import Document
from frappe.contacts.doctype.contact.contact import Contact

from sipgate.sipgate_client import SipgateClient


class SipgateSettings(Document):
	pass


def sync_to_sipgate(doc: Contact, method: Optional[str] = None):
	sipgate_settings = frappe.get_single("Sipgate Settings")
	if not sipgate_settings.enabled:
		return

	payload = get_payload(doc)
	sipgate = SipgateClient(
		sipgate_settings.url, sipgate_settings.token_id, sipgate_settings.get_password("token")
	)

	try:
		if doc.sipgate_id:
			sipgate.update(payload)
		else:
			sipgate.upload(payload)
			id = sipgate.get_sipgate_id(get_contact_number(doc), payload.get("name"))
			frappe.db.set_value(doc.doctype, doc.name, "sipgate_id", id)
	except Exception:
		frappe.log_error(frappe.get_traceback())


def get_payload(contact: Contact) -> frappe._dict:
	payload = {
		"name": f"{contact.get('first_name', '')} {contact.get('last_name', '')}",
		"family": contact.get("last_name", ""),
		"given": contact.get("first_name", ""),
		"emails": [
			{
				"email": email.email_id,
				"type": [is_primary_email(email)],
			}
			for email in contact.email_ids
			if email
		],
		"numbers": [
			{
				"number": phone.phone,
				"type": [is_primary_phone(phone)],
			}
			for phone in contact.phone_nos
			if phone
		],
		"scope": "SHARED",
	}

	if contact.company_name:
		payload.update({"organization": [[contact.company_name]]})

	if contact.get("sipgate_id"):
		payload.update({"id": contact.get("sipgate_id")})

	return frappe._dict(payload)


def get_contact_number(doc) -> Union[str, None]:
	return doc.phone_nos[0].phone if doc.phone_nos else None


def is_primary_phone(phone: object) -> str:
	return "primary" if phone.is_primary_mobile_no or phone.is_primary_phone else ""


def is_primary_email(email: object) -> str:
	return "primary" if email.is_primary else ""


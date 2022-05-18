# Copyright (c) 2022, ALYF GmbH and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.contacts.doctype.contact.contact import Contact

from sipgate.sipgate_client import SipgateClient


class SipgateSettings(Document):
	pass


def sync_to_sipgate(doc: Contact, method: str):
	if method and method != "before_save":
		frappe.log_error(_("Sync to Sipgate was called on event: {}").format(method))
		return

	sipgate_settings = frappe.get_single("Sipgate Settings")
	if not sipgate_settings.enabled:
		return

	phone_numbers = get_phone_numbers(doc)
	full_name = get_full_name(doc)
	if not (phone_numbers and full_name):
		# nothing makes sense if we don't know number + name
		return

	sipgate = SipgateClient(
		sipgate_settings.url,
		sipgate_settings.token_id,
		sipgate_settings.get_password("token"),
	)
	existing_id = doc.get("sipgate_id") or sipgate.get_sipgate_id(
		phone_numbers, full_name
	)
	payload = get_payload(doc)

	try:
		if existing_id:
			sipgate.update(payload, existing_id)
			if existing_id != doc.get("sipgate_id"):
				doc.sipgate_id = existing_id
		else:
			sipgate.upload(payload)
			new_id = sipgate.get_sipgate_id(phone_numbers, full_name)
			doc.sipgate_id = new_id
	except Exception:
		frappe.log_error(frappe.get_traceback())


def get_payload(contact: Contact) -> dict:
	payload = {
		"name": get_full_name(contact),
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

	return payload


def get_phone_numbers(doc) -> "list[str]":
	return [
		row.phone.replace(" ", "").replace("-", "").replace("/", "")
		for row in doc.phone_nos if row.phone
	]


def is_primary_phone(phone: object) -> str:
	return "primary" if phone.is_primary_mobile_no or phone.is_primary_phone else ""


def is_primary_email(email: object) -> str:
	return "primary" if email.is_primary else ""


def get_full_name(contact: Contact) -> str:
	return f"{contact.get('first_name', '')} {contact.get('last_name', '')}"

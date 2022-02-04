# Copyright (c) 2022, ALYF GmbH and contributors
# For license information, please see license.txt

import frappe
import requests
from frappe.model.document import Document
from requests.auth import HTTPBasicAuth
from frappe import _
from typing import Union


class SipgateSettings(Document):
	pass


def sync_to_sipgate(doc=None, method=None):
	sipgate_settings = frappe.get_single("Sipgate Settings")
	if not sipgate_settings.enabled:
		return

	sipgate = Sipgate(sipgate_settings, doc)

	if not doc.sipgate_id:
		sipgate.upload()
		return

	sipgate.update()


class Sipgate:
	def __init__(self, sipgate_settings: SipgateSettings, contact: object) -> None:
		self.sipgate_settings = sipgate_settings
		self.auth = HTTPBasicAuth(
			self.sipgate_settings.token_id, self.sipgate_settings.token
		)
		self.contact = contact

	def upload(self) -> None:
		payload = self.get_payload()
		try:
			response = requests.post(
				url=f"{self.sipgate_settings.url}/contacts",
				json=payload,
				auth=self.auth,
			)
			response.raise_for_status()
			if response.status_code == 201:
				id = self.get_sipgate_id()
				frappe.db.set_value("Contact", self.contact.name, "sipgate_id", id)
		except Exception:
			frappe.msgprint(_("Couldn't sync contact to Sipgate."))

	def update(self) -> None:
		payload = self.get_payload()
		try:
			response = requests.put(
				url=f"{self.sipgate_settings.url}/contacts/{self.contact.sipgate_id}",
				json=payload,
				auth=self.auth,
			)
			response.raise_for_status()
		except Exception:
			frappe.msgprint(_("Couldn't sync contact to Sipgate."))

	def get_sipgate_id(self) -> Union[str, None]:
		response = requests.get(
			url=f"{self.sipgate_settings.url}/contacts",
			data={"phonenumbers": self.get_contact_number()},
			auth=self.auth,
		)

		if response.status_code == 200:
			response = response.json().get("items", [])
			if response:
				return response[0].get("id")

		return None

	def get_contact_number(self) -> Union[str, None]:
		if self.contact.phone_nos:
			return self.contact.phone_nos[0].phone

		return None

	def get_payload(self) -> dict:
		contact_dict = {
			"name": f"{self.contact.get('first_name', '')} {self.contact.get('last_name', '')}",
			"family": self.contact.get("last_name", ""),
			"given": self.contact.get("first_name", ""),
			"emails": [
				{
					"email": email.email_id,
					"type": [is_primary_email(email)],
				}
				for email in self.contact.email_ids
				if email
			],
			"numbers": [
				{
					"number": phone.phone,
					"type": [is_primary_phone(phone)],
				}
				for phone in self.contact.phone_nos
				if phone
			],
			"scope": "SHARED",
		}

		if self.contact.company_name:
			contact_dict.update({"organization": [[self.contact.company_name]]})

		if self.contact.get("sipgate_id"):
			contact_dict.update({"id": self.contact.get("sipgate_id")})

		return contact_dict


def is_primary_phone(phone: object) -> str:
	return "primary" if phone.is_primary_mobile_no or phone.is_primary_phone else ""


def is_primary_email(email: object) -> str:
	return "primary" if email.is_primary else ""


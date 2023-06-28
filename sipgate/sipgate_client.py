# Copyright (c) 2022, ALYF GmbH and contributors
# For license information, please see license.txt

from typing import Union

import requests
from requests.auth import HTTPBasicAuth


class SipgateClient:
	def __init__(
		self,
		sipgate_url: str,
		sipgate_token_id: str,
		sipgate_token: str,
	) -> None:
		self.sipgate_url = sipgate_url
		self.session = requests.Session()
		self.session.auth = HTTPBasicAuth(sipgate_token_id, sipgate_token)
		self.session.headers = {"Accept": "application/json"}

	def request(
		self, method: str, url: str, json: dict = None, params: dict = None
	) -> dict:
		response = self.session.request(method, url, json=json, params=params)
		response.raise_for_status()

		return response.json() if response.text else {}

	def create_contact(self, contact: dict) -> None:
		self.request("POST", f"{self.sipgate_url}/contacts", json=contact)

	def update_contact(self, contact: dict, sipgate_id: str) -> None:
		self.request("PUT", f"{self.sipgate_url}/contacts/{sipgate_id}", json=contact)

	def delete_contact(self, sipgate_id: str) -> None:
		self.request("DELETE", f"{self.sipgate_url}/contacts/{sipgate_id}")

	def get_sipgate_id(
		self, phonenumbers: "list[str]", full_name: str
	) -> Union[str, None]:
		if not phonenumbers:
			return None

		response = self.request(
			"GET",
			f"{self.sipgate_url}/contacts",
			params={"phonenumbers": phonenumbers},
		)
		items = [
			item
			for item in response.get("items", [])
			if item.get("name", "") == full_name
		]

		return items[0].get("id") if items else None

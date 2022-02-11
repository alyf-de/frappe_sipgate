# Copyright (c) 2022, ALYF GmbH and contributors
# For license information, please see license.txt

import requests
from requests.auth import HTTPBasicAuth
from typing import Union


class SipgateClient:
	def __init__(
		self,
		sipgate_url: str,
		sipgate_token_id: str,
		sipgate_token: str,
		contact: object,
	) -> None:
		self.sipgate_url = sipgate_url
		self.sipgate_token_id = sipgate_token_id
		self.sipgate_token = sipgate_token
		self.contact = contact

	@property
	def auth(self):
		return HTTPBasicAuth(self.sipgate_token_id, self.sipgate_token)

	def upload(self) -> None:
		response = requests.post(
			url=f"{self.sipgate_url}/contacts",
			json=self.contact,
			auth=self.auth,
		)
		response.raise_for_status()

	def update(self) -> None:
		response = requests.put(
			url=f"{self.sipgate_url}/contacts/{self.contact.sipgate_id}",
			json=self.contact,
			auth=self.auth,
		)
		response.raise_for_status()

	def get_sipgate_id(self, phonenumbers: str) -> Union[str, None]:
		if not phonenumbers:
			return None

		response = requests.get(
			url=f"{self.sipgate_url}/contacts",
			data={"phonenumbers": phonenumbers},
			auth=self.auth,
		)
		response.raise_for_status()

		response = response.json().get("items", [])
		return response[0].get("id") if response else None


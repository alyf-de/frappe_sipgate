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
		self.sipgate_token_id = sipgate_token_id
		self.sipgate_token = sipgate_token

	@property
	def auth(self):
		return HTTPBasicAuth(self.sipgate_token_id, self.sipgate_token)

	def upload(self, contact: object) -> None:
		response = requests.post(
			url=f"{self.sipgate_url}/contacts",
			json=contact,
			auth=self.auth,
		)
		response.raise_for_status()

	def update(self, contact: object) -> None:
		response = requests.put(
			url=f"{self.sipgate_url}/contacts/{self.contact.sipgate_id}",
			json=contact,
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


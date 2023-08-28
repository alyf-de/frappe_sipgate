Sync contacts from Frappe/ERPNext to Sipgate.

When a contact is created or updated in ERPNext:

1. Check if the numbers are already in Sipgate contacts.
2. Update existing contact or create a new one.
3. Store (or update) the contact's Sipgate ID.

When a contact is deleted in ERPNext:

1. Check if it has a Sipgate ID, abort if not.
2. Delete contact in Sipgate.

## Gotchas

Phone numbers must be entered with country code (for example, "+49 341-39285850").

Before transmission to Sipgate all whitespaces (`" "`), slashes (`"/"`) and dashes (`"-"`) will be removed from the phone number.

## Legal

This repository is licensed under GPLv3.

Sipgate is a trademark of [sipgate GmbH](https://www.sipgate.de/). This integration is not endorsed or approved in any way by Sipgate.

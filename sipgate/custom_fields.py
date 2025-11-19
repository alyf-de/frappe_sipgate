from sipgate.utils import identity as _


def get_custom_fields():
	return {
		"Contact": [
			{
				"fieldname": "sipgate_id",
				"fieldtype": "Data",
				"label": _("Sipgate ID"),
				"insert_after": "unsubscribed",
				"read_only": 1,
				"translatable": 0,
				"no_copy": 1,
				"unique": 1,
			}
		],
	}

// Copyright (c) 2025, karthik and contributors
// For license information, please see license.txt

frappe.query_reports["Machine Maintenance Report"] = {
	"filters": [
		{
			"fieldname": "machine_name",
			"label": "Machine",
			"fieldtype": "Link",
			"options": "Item",
		},
		{
			"fieldname": "technician",
			"label": "Technician",
			"fieldtype": "Link",
			"options": "Employee",
		},
		{
			"fieldname": "from_date",
			"label": "From Date",
			"fieldtype": "Date",
		},
		{
			"fieldname": "to_date",
			"label": "To Date",
			"fieldtype": "Date",
		},
		{
			"fieldname": "consolidated",
			"label": "Consolidated",
			"fieldtype": "Check",
		}
	]
};

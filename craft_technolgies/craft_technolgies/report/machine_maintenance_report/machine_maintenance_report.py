# Copyright (c) 2025, karthik and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    filters = filters or {}

    if filters.get("consolidated"):
        columns = get_consolidated_columns()
        data = get_consolidated_data(filters)
    else:
        columns = get_detailed_columns()
        data = get_detailed_data(filters)

    return columns, data


def get_detailed_data(filters):
    conditions = []
    values = {}

    if filters.get("machine_name"):
        conditions.append("mm.machine_name = %(machine_name)s")
        values["machine_name"] = filters["machine_name"]

    if filters.get("technician"):
        conditions.append("mm.technician = %(technician)s")
        values["technician"] = filters["technician"]

    if filters.get("from_date") and filters.get("to_date"):
        conditions.append("mm.maintenance_date BETWEEN %(from_date)s AND %(to_date)s")
        values["from_date"] = filters["from_date"]
        values["to_date"] = filters["to_date"]

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    query = f"""
        SELECT
            mm.machine_name,
            mm.maintenance_date,
            mm.technician,
            mm.status,
            mm.cost,
            CASE
                WHEN mm.status = 'Overdue' THEN 'red'
                WHEN mm.status = 'Scheduled' THEN 'yellow'
                WHEN mm.status = 'Completed' THEN 'green'
                ELSE ''
            END AS _row_color
        FROM
            `tabMachine Maintenance` mm
        WHERE
            {where_clause}
        ORDER BY
            mm.maintenance_date DESC
    """

    return frappe.db.sql(query, values, as_dict=True)


def get_detailed_columns():
    return [
        {
            "fieldname": "machine_name",
            "label": "Machine",
            "fieldtype": "Link",
            "options": "Item",
            "width": 200,
        },
        {
            "fieldname": "maintenance_date",
            "label": "Maintenance Date",
            "fieldtype": "Date",
            "width": 150,
        },
        {
            "fieldname": "technician",
            "label": "Technician",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 150,
        },
        {
            "fieldname": "status",
            "label": "Status",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "fieldname": "cost",
            "label": "Total Cost",
            "fieldtype": "Currency",
            "width": 120,
        }
    ]


def get_consolidated_data(filters):
    conditions = []
    values = {}

    if filters.get("machine_name"):
        conditions.append("machine_name = %(machine_name)s")
        values["machine_name"] = filters["machine_name"]

    if filters.get("technician"):
        conditions.append("technician = %(technician)s")
        values["technician"] = filters["technician"]

    if filters.get("from_date") and filters.get("to_date"):
        conditions.append("maintenance_date BETWEEN %(from_date)s AND %(to_date)s")
        values["from_date"] = filters["from_date"]
        values["to_date"] = filters["to_date"]

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    query = f"""
        SELECT
            machine_name,
            COUNT(*) AS maintenance_count,
            SUM(cost) AS total_cost
        FROM
            `tabMachine Maintenance`
        WHERE
            {where_clause}
        GROUP BY
            machine_name
        ORDER BY
            machine_name
    """

    return frappe.db.sql(query, values, as_dict=True)


def get_consolidated_columns():
    return [
        {
            "fieldname": "machine_name",
            "label": "Machine",
            "fieldtype": "Link",
            "options": "Item",
            "width": 200,
        },
        {
            "fieldname": "maintenance_count",
            "label": "Maintenance Count",
            "fieldtype": "Int",
            "width": 150,
        },
        {
            "fieldname": "total_cost",
            "label": "Total Cost",
            "fieldtype": "Currency",
            "width": 150,
        }
    ]

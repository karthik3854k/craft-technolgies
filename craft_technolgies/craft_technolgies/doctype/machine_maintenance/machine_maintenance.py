# Copyright (c) 2025, karthik and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.desk.notifications import notify_mentions
from frappe.utils import cstr, now, today


class MachineMaintenance(Document):
	@frappe.whitelist()
	def add_note(self, note):
		self.append("notes", {"note": note, "added_by": frappe.session.user, "added_on": now()})
		self.save()
		notify_mentions(self.doctype, self.name, note)


	

     

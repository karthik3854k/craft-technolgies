// Copyright (c) 2025, karthik and contributors
// For license information, please see license.txt

frappe.ui.form.on("Machine Maintenance", {
	refresh(frm) {
        if (!frm.is_new() && frm.doc.docstatus === 0) {
            frm.add_custom_button(__("Mark Completed"), function () {
                frm.set_value("status", "Completed");
                frm.set_value("completion_date", frappe.datetime.get_today());
                frappe.show_alert({message: __("Status set to Completed"), indicator: 'green'});
                frm.save();
            });
        }
        frm.events.show_notes(frm);
    },
    show_notes(frm) {
        if (frm.doc.docstatus == 1) return;

        const crm_notes = new erpnext.utils.CRMNotes({
            frm: frm,
            notes_wrapper: $(frm.fields_dict.notes_html.wrapper),
        });
        crm_notes.refresh();
    },
    before_save(frm) {
        if (frm.doc.status != "Completed" && frm.doc.maintenance_date < frappe.datetime.get_today()) {
            frm.set_value("status", "Overdue");
        }
    },
    before_workflow_action(frm) {
        if (frm.selected_workflow_action == "Close") {
            if (!frm.doc.technician) {
                frappe.throw(__("Technician is required before completing the maintenance record."));
            }
        }
    }
});


	

frappe.ui.form.on("Machine Maintenance Part", {
    quantity(frm, cdt, cdn) {
        update_amount(frm, cdt, cdn);
    },
    rate(frm, cdt, cdn) {
        update_amount(frm, cdt, cdn);
    }
});


function update_amount(frm, cdt, cdn) {
    let row = frappe.get_doc(cdt, cdn);
    row.amount = (row.quantity || 0) * (row.rate || 0);
    frappe.model.set_value(cdt, cdn, "amount", row.amount);
    calculate_total_amount(frm);
}

function calculate_total_amount(frm) {
    let total = 0;

    (frm.doc.parts_used || []).forEach(row => {
        total += row.amount || 0;
    });

    frm.set_value("cost", total);
}

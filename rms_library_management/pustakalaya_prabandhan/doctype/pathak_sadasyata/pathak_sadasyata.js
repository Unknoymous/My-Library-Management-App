// Copyright (c) 2026, RadhaMadhav and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Pathak Sadasyata", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Pathak Sadasyata', {
 refresh: function(frm) {
 frm.add_custom_button('Create Membership', () => {
 frappe.new_doc('Pathak Sadasyata', {
 library_member: frm.doc.name
 })
 })
 frm.add_custom_button('Create Transaction', () => {
 frappe.new_doc('Len Den', {
 library_member: frm.doc.name
 })
 })
 }
});

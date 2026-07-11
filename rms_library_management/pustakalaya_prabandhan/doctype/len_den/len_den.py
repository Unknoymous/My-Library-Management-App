import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus
from frappe.utils import getdate


class LenDen(Document):

    def before_submit(self):

        if self.type == "Issued":

            self.validate_membership()
            self.validate_issue()
            self.validate_maximum_limit()

            lekh = frappe.get_doc("Lekh", self.lekh)
            lekh.status = "Issued"
            lekh.save()

        elif self.type == "Returned":

            self.validate_return()

            lekh = frappe.get_doc("Lekh", self.lekh)
            lekh.status = "Available"
            lekh.save()

    def validate_issue(self):

        lekh = frappe.get_doc("Lekh", self.lekh)

        if lekh.status == "Issued":
            frappe.throw("This Lekh has already been issued.")

    def validate_return(self):

        lekh = frappe.get_doc("Lekh", self.lekh)

        if lekh.status == "Available":
            frappe.throw("This Lekh is already available.")

    def validate_membership(self):

        membership = frappe.get_doc(
            "Pathak Sadasyata",
            self.pathak_sadasyata
        )

        if membership.docstatus != DocStatus.submitted():
            frappe.throw("Membership is not submitted.")

        transaction_date = getdate(self.datetime)

        if transaction_date < membership.from_date:
            frappe.throw("Membership has not started yet.")

        if transaction_date > membership.to_date:
            frappe.throw("Membership has expired.")

    def validate_maximum_limit(self):

        max_lekhs = frappe.db.get_single_value(
            "Pustakalaya Settings",
            "max_lekhs"
        )

        issued_count = frappe.db.count(
            "Len Den",
            {
                "pathak_sadasyata": self.pathak_sadasyata,
                "type": "Issued",
                "docstatus": DocStatus.submitted(),
            },
        )

        if issued_count >= max_lekhs:
            frappe.throw(
                f"Maximum limit of {max_lekhs} issued Lekhs reached."
            )
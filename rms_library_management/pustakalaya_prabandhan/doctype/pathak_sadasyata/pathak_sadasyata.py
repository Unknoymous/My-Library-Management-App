import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus
from frappe.utils import add_days


class PathakSadasyata(Document):

    def before_submit(self):

        # Fetch Pathak details
        pathak = frappe.get_doc("Pathak", self.pathak)

        # Automatically fill full name
        self.pura_naam = pathak.pura_naam

        # Check for overlapping memberships
        exists = frappe.db.exists(
            "Pathak Sadasyata",
            {
                "pathak": self.pathak,
                "docstatus": DocStatus.submitted(),
                "to_date": (">", self.from_date),
            },
        )

        if exists:
            frappe.throw("There is already an active membership for this Pathak.")

        # Calculate expiry date
        rin_awadhi = frappe.db.get_single_value(
            "Pustakalaya Settings",
            "rin_awadhi"
        )

        self.to_date = add_days(self.from_date, rin_awadhi or 30)
# Copyright (c) 2026, RadhaMadhav and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Pathak(Document):
    #this method will run every time a document is saved
    def before_save(self):
        self.pura_naam = f'{self.pehla_naam} {self.aakhri_naam or ""}'

from frappe.email.doctype.newsletter.newsletter import Newsletter
import frappe
from datetime import datetime


class SaasEmailNewsLetter(Newsletter):
    def before_save(self):
        # Check if self.email_group exists and is valid
        # if hasattr(self, 'email_group') and isinstance(self.email_group, list):
        #     frappe.msgprint(frappe.as_json(self.email_group))
        # else:
        #     frappe.msgprint("No valid email group found")
        total_subscriber = self.get_current_total_subscriber()
        total_current_month_subscriber= self.get_current_month_total_subscriber()
        frappe.msgprint(frappe.as_json(total_current_month_subscriber))
        frappe.msgprint(frappe.as_json(total_subscriber))
        # print(total_subscriber)
        # frappe.msgprint(f"Total Subscribers: {total_subscriber}")
        

    def get_current_total_subscriber(self):
        # Safeguard to ensure self.email_group is a list
        if hasattr(self, 'email_group') and isinstance(self.email_group, list):
            # Sum the total_subscribers from the email group
            total_subscriber = sum(item.get('total_subscribers', 0) for item in self.email_group)
            return total_subscriber
        else:
            frappe.msgprint("No valid email group found")
            return 0
    def get_current_month_total_subscriber(self):
        current_year = datetime.now().year
        current_month = datetime.now().month
        company =self.company

        result = frappe.db.sql(
            """
            SELECT  eg.email_group, SUM(CAST(eg.total_subscribers AS UNSIGNED)) AS total_subscribers_sum
            FROM `tabNewsletter` AS nwl
            LEFT JOIN `tabNewsletter Email Group` AS eg
            ON nwl.name = eg.parent
            WHERE YEAR(nwl.creation) = %s AND MONTH(nwl.creation) = %s AND nwl.company= %s
            GROUP BY nwl.name
            """,
            (current_year, current_month,company),
            as_dict=True
        )
        return sum(item ['total_subscribers_sum'] for item in result)
    def get_total_allocated_email(self):
        company=self.company
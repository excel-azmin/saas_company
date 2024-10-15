from frappe.email.doctype.newsletter.newsletter import Newsletter
import frappe
from datetime import datetime


class SaasEmailNewsLetter(Newsletter):
    def before_save(self):
        total_subscriber = self.get_current_total_subscriber()
        total_current_month_subscriber = self.get_current_month_total_subscriber()
        get_total_allocated_mail = frappe.db.get_value('Company Email Allocation', self.custom_company, 'allocated')
        get_total_subscribe_mail= total_subscriber+ total_current_month_subscriber
        if get_total_allocated_mail < get_total_subscribe_mail:
            frappe.throw('Email Allocation limit exceeded for the month.')

    def get_current_total_subscriber(self):
        # Safeguard to ensure self.email_group is a list
        if hasattr(self, 'email_group') and isinstance(self.email_group, list):
            # Sum the total_subscribers from the email group, ensuring conversion to int
            total_subscriber = sum(int(item.get('total_subscribers', 0)) for item in self.email_group if item.get('total_subscribers'))
            return total_subscriber
        else:
            frappe.msgprint("No valid email group found")
            return 0

    def get_current_month_total_subscriber(self):
        current_year = datetime.now().year
        current_month = datetime.now().month
        company = str(self.custom_company)

        result = frappe.db.sql(
            """
            SELECT eg.email_group, SUM(CAST(eg.total_subscribers AS UNSIGNED)) AS total_subscribers_sum
            FROM `tabNewsletter` AS nwl
            LEFT JOIN `tabNewsletter Email Group` AS eg
            ON nwl.name = eg.parent
            WHERE YEAR(nwl.creation) = %s AND MONTH(nwl.creation) = %s AND nwl.custom_company= %s
            GROUP BY nwl.name
            """,
            (current_year, current_month, company),
            as_dict=True
        )
        return sum(item['total_subscribers_sum'] for item in result)



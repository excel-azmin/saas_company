import requests
import json
import frappe
from datetime import datetime

def setup_webhook_url():
    print('work')
def delete_webhook_url():
    print('delete')
    
    
    
@frappe.whitelist(allow_guest=True)
def create_appointment(calendly_data):
    appointment_data = json.loads(calendly_data)
    frappe.msgprint(frappe.as_json(appointment_data))
    
    new_appointment = frappe.get_doc({
        'doctype': 'Appointment',
        'client_name': appointment_data['payload']['name'],
        'appointment_time': appointment_data['payload']['start_time'],
        'duration': appointment_data['payload']['duration'],
        # Add other necessary fields
    })
    
    new_appointment.insert()
    frappe.db.commit()
    return new_appointment.name
@frappe.whitelist(allow_guest=True)
def get_weebhook_url_list():
    return {"test":"test"}
@frappe.whitelist(allow_guest=True)
def get_current_month_total_newsletter_mail(company):
    current_year = datetime.now().year
    current_month = datetime.now().month

    result = frappe.db.sql(
        """
        SELECT eg.email_group, SUM(CAST(eg.total_subscribers AS UNSIGNED)) AS total_subscribers_sum
        FROM `tabNewsletter` AS nwl
        LEFT JOIN `tabNewsletter Email Group` AS eg
        ON nwl.name = eg.parent
        WHERE YEAR(nwl.creation) = %s AND MONTH(nwl.creation) = %s AND nwl.custom_company = %s
        GROUP BY nwl.name
        """,
        (current_year, current_month, company),
        as_dict=True
    )

    # Ensure that we are returning a meaningful result
    return sum(item['total_subscribers_sum'] for item in result) if result else 0

@frappe.whitelist(allow_guest=True)
def test(company):
    return company
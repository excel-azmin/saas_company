import requests
import json
import frappe

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

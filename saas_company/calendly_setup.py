import requests
import json
import frappe

# Fetch Calendly API token from Frappe's 'Calendly Settings' doctype
calendly_settings = frappe.get_doc('Calendly Settings')

# Base URLs for Calendly API (v2) and webhook URL
calendly_base_url = "https://api.calendly.com"
get_host_url=frappe.utils.get_url().replace("http://", "https://") 
demo_site="https://mark-erp.arcapps.org"
webhook_url = f"{demo_site}/api/method/saas_company.api.create_appointment"

# Headers with Authorization token and content type
headers = {
    "Authorization": f"Bearer {calendly_settings.get('api_token')}",
    "Content-Type": "application/json"
}

# Function to retrieve organization URL
def get_organization_url():
    user_url = f"{calendly_base_url}/users/me"
    try:
        response = requests.get(user_url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            organization_url = user_data['resource']['current_organization']  # Get the organization URL
            return organization_url
        else:
            print(f"Failed to retrieve organization URL: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Error while retrieving organization URL: {e}")
        return None

# Function to set up a webhook in Calendly
def setup_webhook_url():
    organization_url = get_organization_url()
    if not organization_url:
        print("Organization URL not found. Cannot proceed with webhook setup.")
        return

    data = {
        "url": webhook_url,
        "events": [
            "invitee.created",   # Trigger when a new invitee (appointment) is created
            "invitee.canceled"   # Trigger when an invitee cancels an appointment
        ],
        "organization": organization_url,  # Set the organization URL
        "scope": "organization"  # You can change the scope to 'organization' if needed
    }

    try:
        response = requests.post(f"{calendly_base_url}/webhook_subscriptions", headers=headers, data=json.dumps(data))
        if response.status_code == 201:
            print("Webhook setup successful:", response.json())
        else:
            print("Failed to set up webhook:", response.status_code, response.text)
    except Exception as e:
        print(f"Error while setting up webhook: {e}")

# Example usage:
# setup_webhook_url()

import frappe

def create_allocated_company_child_doctype():
    # Check if the child doctype 'Allocated Company' already exists
    if not frappe.db.exists('DocType', {'name': 'Allocated Company'}):
        # Create the child doctype 'Allocated Company'
        allocated_company_doctype = frappe.get_doc({
            'doctype': 'DocType',
            'name': 'Allocated Company',
            'module': 'Custom',  # You can change this to the appropriate module name
            'istable': 1,
            'custom': 1,# Marks this as a child doctype (table)
            'fields': [
                {
                    'fieldname': 'company',
                    'fieldtype': 'Link',
                    'label': 'Company',
                    'options': 'Company',
                    'in_list_view': 1,  # Shows the field in the list view
                    'reqd': 1  # Mandatory field
                }
            ],
            # 'permissions': [
            #     {
            #         'role': 'System Manager',  # Set appropriate roles
            #         'read': 1,
            #         'write': 1,
            #         'create': 1,
            #         'delete': 1
            #     }
            # ]
        })

        # Insert the new child doctype
        allocated_company_doctype.insert(ignore_permissions=True)
        print("Child Doctype 'Allocated Company' has been created successfully.")

    else:
        print("Child Doctype 'Allocated Company' already exists.")


def add_allocated_company_table_to_all_doctypes():
    # Get a list of all doctypes in the ERPNext system
    create_allocated_company_child_doctype()
    all_doctypes = frappe.get_all('DocType', filters={'issingle': 0})
    if not frappe.db.exists('Custom Field', {'dt': 'User', 'fieldname': 'allocated_companies'}):
                # Create a new custom field 'Allocated Companies' of type 'Table'
                custom_field = frappe.get_doc({
                    'doctype': 'Custom Field',
                    'dt': 'User',
                    'label': 'Allocated Companies',
                    'fieldname': 'allocated_companies',
                    'fieldtype': 'Table MultiSelect',
                    'options': 'Allocated Company',  # Link to the Allocated Company child doctype
                    'insert_after': 'modified',  # Insert after 'modified' field or choose another appropriate field
                    'read_only': 0
                })
                custom_field.insert(ignore_permissions=True)
                print("added table ")# Excludes single doctypes

    for doctype in all_doctypes:
        doctype_name = doctype['name']

        try:
            # Check if the 'Allocated Company' table field already exists for the doctype
            if not frappe.db.exists('Custom Field', {'dt': doctype_name, 'fieldname': 'allocated_company'}):
                # Create a new custom field 'Allocated Companies' of type 'Table'
                custom_field = frappe.get_doc({
                    'doctype': 'Custom Field',
                    'dt': doctype_name,
                    'label': 'Allocated Company',
                    'fieldname': 'allocated_company',
                    'fieldtype': 'Link',
                    'options': 'Company',  # Link to the Allocated Company child doctype
                    'insert_after': 'modified',  # Insert after 'modified' field or choose another appropriate field
                    'read_only': 1,
                     
                })
                custom_field.insert(ignore_permissions=True)
                print(f"Added 'Allocated Company'  to {doctype_name}")
        except frappe.DoesNotExistError as e:
            print(f"Skipping {doctype_name} due to missing module: {str(e)}")
        except Exception as e:
            print(f"Error processing {doctype_name}: {str(e)}")

    # Commit the changes to the database
    frappe.db.commit()


def remove_allocated_company_table_from_all_doctypes():
    # Get a list of all doctypes in the ERPNext system
    all_doctypes = frappe.get_all('DocType', filters={'issingle': 0})  # Excludes single doctypes

    for doctype in all_doctypes:
        doctype_name = doctype['name']

        # Check if the 'Allocated Companies' field exists for the doctype
        custom_field = frappe.db.exists('Custom Field', {'dt': doctype_name, 'fieldname': 'allocated_company'})
        if custom_field:
            # Delete the custom field
            frappe.delete_doc('Custom Field', custom_field)
            print(f"Deleted 'Allocated Company'from {doctype_name}")

    # Commit the changes to the database
    frappe.db.commit()

def test(doc, event):
    core_doctypes = frappe.get_all('DocType', filters={ 'module': ["in", ["Automation", "Contacts", "Core", "Custom", "Desk", "Email", "Event Streaming", "Geo", "Integrations", "Printing", "Social", "Website", "Workflow"]]}, fields=['name'])
    core_doctypes_name = [item['name'] for item in core_doctypes]  
    if doc.doctype in core_doctypes_name:
        return 
    """
    Adds allocated companies to the document if they don't already exist.
    Skips processing for the "User" doctype to avoid recursion.
    Only works when the document is new.
    """

    # Check if the function is already running
    # if frappe.flags.in_test_function:
    #     return
    
    # Check if this is a new document
    is_new_document = doc.get("__islocal")
    if not is_new_document:
        return

    try:
        # Get the current user and their allocated companies
        user = frappe.get_doc("User", frappe.session.user)
        allocated_companies = user.get("allocated_companies") or []
        if len(allocated_companies) > 0:
            return
        frappe.msgprint(frappe.as_json(allocated_companies))
        company=allocated_companies[0]
        
        frappe.db.set_value(doc.doctype,doc.name,"allocated_company",company.company)

        # Print a message indicating the start of the process
        frappe.msgprint('Starting to process allocated companies.')


    except Exception as e:
        # Handle any exception that occurs and display an error message
        frappe.log_error(f"Error in test function: {str(e)}")
        frappe.throw(f"An error occurred while adding allocated companies: {str(e)}")
def check_user_allocated_company(doc,event):
    # user = frappe.get_doc("User", frappe.session.user)
    
    # frappe.msgprint(frappe.as_json(user))
    allocated_companies = doc.get("allocated_companies")
    if len(allocated_companies) >1:
        frappe.throw("You cannot add here multiple company")


       














import frappe

def create_allocated_company_child_doctype():
    # Check if the child doctype 'Allocated Company' already exists
    if not frappe.db.exists('DocType', {'name': 'Allocated Company'}):
        # Create the child doctype 'Allocated Company'
        allocated_company_doctype = frappe.get_doc({
            'doctype': 'DocType',
            'name': 'Allocated Company',
            'module': 'Saas Company',  # You can change this to the appropriate module name
            'istable': 1,  # Marks this as a child doctype (table)
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
            'permissions': [
                {
                    'role': 'System Manager',  # Set appropriate roles
                    'read': 1,
                    'write': 1,
                    'create': 1,
                    'delete': 1
                }
            ]
        })

        # Insert the new child doctype
        allocated_company_doctype.insert(ignore_permissions=True)
        print("Child Doctype 'Allocated Company' has been created successfully.")

    else:
        print("Child Doctype 'Allocated Company' already exists.")


def add_allocated_company_table_to_all_doctypes():
    # Get a list of all doctypes in the ERPNext system
    all_doctypes = frappe.get_all('DocType', filters={'issingle': 0})  # Excludes single doctypes

    for doctype in all_doctypes:
        doctype_name = doctype['name']

        try:
            # Check if the 'Allocated Company' table field already exists for the doctype
            if not frappe.db.exists('Custom Field', {'dt': doctype_name, 'fieldname': 'allocated_companies'}):
                # Create a new custom field 'Allocated Companies' of type 'Table'
                custom_field = frappe.get_doc({
                    'doctype': 'Custom Field',
                    'dt': doctype_name,
                    'label': 'Allocated Companies',
                    'fieldname': 'allocated_companies',
                    'fieldtype': 'Table',
                    'options': 'Allocated Company',  # Link to the Allocated Company child doctype
                    'insert_after': 'modified',  # Insert after 'modified' field or choose another appropriate field
                    'read_only': 0
                })
                custom_field.insert(ignore_permissions=True)
                print(f"Added 'Allocated Companies' table to {doctype_name}")
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
        custom_field = frappe.db.exists('Custom Field', {'dt': doctype_name, 'fieldname': 'allocated_companies'})
        if custom_field:
            # Delete the custom field
            frappe.delete_doc('Custom Field', custom_field)
            print(f"Deleted 'Allocated Companies' table from {doctype_name}")

    # Commit the changes to the database
    frappe.db.commit()
def test():
    print('work')


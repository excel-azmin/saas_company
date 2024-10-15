frappe.ui.form.on('Company Email Allocation', {
    refresh: function(frm) {
        frm.add_custom_button(__('Open Integer Prompt'), function() {
            let d = new frappe.ui.Dialog({
                title: 'Integer Input Dialog',
                fields: [
                    {
                        label: 'Amount',
                        fieldname: 'integer_input',
                        fieldtype: 'Int',
                        reqd: 1,  // Make the integer input required
                        default: 0  // Default value
                    },
                    {
                        label: 'Increase',
                        fieldname: 'increase_check',
                        fieldtype: 'Check'
                    },
                    {
                        label: 'Decrease',
                        fieldname: 'decrease_check',
                        fieldtype: 'Check'
                    }
                ],
                primary_action_label: 'Submit',
                primary_action(values) {
                    // Ensure the integer input is valid and required
                    if (isNaN(values.integer_input) || values.integer_input === '') {
                        frappe.msgprint(__('Please enter a valid integer.'));
                        return;
                    }

                    // Ensure only one of the checkboxes is checked
                    if (values.increase_check && values.decrease_check) {
                        frappe.msgprint(__('You cannot check both Increase and Decrease at the same time.'));
                        return;
                    }
					if (!values.increase_check || !values.decrease_check) {
                        frappe.msgprint(__('Select Increase or Decrease '));
                        return;
                    }

                    // Handle the integer input and increment/decrement logic
                    let result = values.integer_input;

                    if (values.increase_check) {
                        result += 1;  // Increase the integer value
                    } else if (values.decrease_check) {
                        result -= 1;  // Decrease the integer value
                    }

                    frappe.msgprint('You entered: ' + result);
                    d.hide();
                }
            });

            // Logic to prevent checking both checkboxes
            d.fields_dict.increase_check.$input.on('change', function() {
                if (d.get_value('increase_check')) {
                    d.set_value('decrease_check', 0);  // Uncheck Decrease when Increase is checked
                }
            });

            d.fields_dict.decrease_check.$input.on('change', function() {
                if (d.get_value('decrease_check')) {
                    d.set_value('increase_check', 0);  // Uncheck Increase when Decrease is checked
                }
            });

            d.show();
        });
        const company = frm.doc.company
        if(company){
            frappe.call({
                method: "saas_company.api.get_current_month_total_newsletter_mail",
                args: {
                    company: company // Replace with actual company name
                },
                callback: function(response) {
                    // Handle the response here
                    if(response.message) {
                        const remaining= frm.doc.allocated - response.message
                        frm.set_value('remaining',remaining)
                        frm.refresh_field("remaining")
                    }
                },
                error: function(error) {
                    console.log("An error occurred:", error);
                }
            });
        }
    }
});

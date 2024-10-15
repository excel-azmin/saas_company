frappe.ui.form.on('Company Email Allocation', {
    refresh: function(frm) {
        frm.add_custom_button(__('Adjust Allocation'), function() {
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
                    console.log(values)
                    // Ensure the integer input is valid and required
                    if (isNaN(values.integer_input) || values.integer_input === '') {
                        frappe.msgprint(__('Please enter a valid integer.'));
                        return;
                    }

                    // Ensure only one of the checkboxes is checked
                    // Handle the integer input and increment/decrement logic
                    let result = frm.doc.allocated;

                    if (values.increase_check) {
                        result += values.integer_input; 
                        frm.set_value("allocated",result) // Increase the integer value
                    } else if (values.decrease_check ) {
                        result -= values.integer_input;
                        frm.set_value("allocated",result)   // Decrease the integer value
                    }

                    frappe.msgprint('You entered: ' + result);
                    frm.save()
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
        if(company && !frm.is_new()){
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
                        frm.save()
                    }
                },
                error: function(error) {
                    console.log("An error occurred:", error);
                }
            });
        }
    }
});

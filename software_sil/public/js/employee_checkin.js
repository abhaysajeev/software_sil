frappe.web_form.after_load = () => {
    // Dynamically get the logged-in user (employee name) and set it to the employee_name field
    // var employeeName = frappe.session.user;
    // frappe.web_form.set_value('employee_name', employeeName);

    // Add a custom button using jQuery
    var r = $('<input type="button" value="Show Attendance"/>');

    // Append the button to the Web Form's actions section
    $(".web-form-head .web-form-actions").append(r);

    // Set up the button click event
    r.on('click', function() {
        // Action to take when the button is clicked
        frappe.msgprint(__('Button clicked!'));
    });
};


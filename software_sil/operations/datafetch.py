import frappe

"""
tabSalaryAmtCalculator                            
tabSalaryAmtMonths                                
tabSalaryCalculator                               
tabSalaryCalculator Item                         
tabSalaryCalculator MonthAmt                      
tabSalaryCalculatorMonths 
"""
@frappe.whitelist(allow_guest= True)
def get_data():
    doc_data = frappe.db.sql("""SELECT 'employee_name', 'salary_' FROM `tabSalaryAmtCalculator` WHERE name = '003'""", as_dict=True)

    return doc_data


@frappe.whitelist(allow_guest= True)
def get_employee_data():
    doc_data = frappe.db.sql("""SELECT * FROM `tabSalaryCalculatorMonths`""", as_dict=True)

    return doc_data

@frappe.whitelist(allow_guest= True)
def get_salary_data():
    doc_data = frappe.db.sql("""SELECT 
                             S.employee_name,
                             
                             S.total_salary,
                             C.month,
                             C.sal_amount,
                             C.sal_bonus
                
                             FROM `tabSalaryAmtCalculator` S
                             LEFT JOIN `tabSalaryCalculatorMonths` C on C.parent = S.name
                             """, as_dict=True)

    return doc_data

@frappe.whitelist(allow_guest=True)
def get_employee_data_new():
    # Fetch the parent data (SalaryAmtCalculator records)
    doc_data = frappe.db.sql("""SELECT 
                             name,
                             employee_name,
                             total_salary
                             FROM `tabSalaryAmtCalculator`
                             """, as_dict=True)

    result = []

    # Loop through each parent record
    for data in doc_data:
        # Fetch the related child data (SalaryCalculatorMonths records)
        child_data = frappe.db.sql("""
            SELECT 
            parent,                      
            month,
            sal_amount,
            sal_bonus,
            sal_total_amount                                                                                            
            FROM `tabSalaryCalculatorMonths`
            WHERE parent = %s
        """, (data['name'],), as_dict=True)

        # Add the child data as a key to the parent data
        data['monthly_pay'] = child_data

        # Append the updated parent data (with the nested child data) to the result list
        result.append(data)

    # Return the final result with nested child data
    return result


@frappe.whitelist(allow_guest=True)
def get_existing_records():
    # Query the existing records from the SalaryAmtCalculator doctype
    records = frappe.db.sql("""
        SELECT name, employee_name, total_salary
        FROM `tabSalaryAmtCalculator`
    """, as_dict=True)

    return records
    
@frappe.whitelist(allow_guest=True)
def getInvoiceDetails():
    records = frappe.db.sql("""
            SELECT
                si.name,
                si.docstatus,
                si.currency,
                si.customer_name,
                si.grand_total,
                si.total_taxes_and_charges,
                si.posting_date,
                si.net_total,
                si.paid_amount,
                si.total_advance,
                si.custom_zone,
                si.custom_zonal_manager,
                si.custom_region,
                si.custom_regional_manager,
                si.custom_cluster,
                si.custom_cluster_manager,
                c.customer_type,
                c.customer_group,    
                c.custom_customer_category,
                c.custom_state,
                c.tax_category,
                c.default_currency,                
                COALESCE(si.outstanding_amount, 0.0) AS outstanding_amount,
                si.total 
            FROM
                `tabSales Invoice` si 
            LEFT JOIN `tabCustomer` c ON c.name = si.customer_name 
            WHERE si.posting_date BETWEEN '2024-05-11' AND '2024-12-11'
 
            ORDER BY si.posting_date DESC
        """, as_dict=True)
        
    return records

@frappe.whitelist(allow_guest=True)
def get_sales_invoice_data():
    # Hardcoded filters (you can modify these filters as needed each time)
    filters = {
 
  
  'starting_posting_date': '2020-12-11',
  'ending_posting_date': '2024-12-11',
  'custom_cluster_manager': 'MOHOMED RIAZ KHAN'
    }

    try:
        # List to store the conditions for the WHERE clause
        conditions = []
        query_params = []

        # Dynamically add conditions for each filter key
        if filters.get('custom_zonal_manager'):
            conditions.append("si.custom_zonal_manager = %s")
            query_params.append(filters['custom_zonal_manager'])

        if filters.get('custom_regional_manager'):
            conditions.append("si.custom_regional_manager = %s")
            query_params.append(filters['custom_regional_manager'])

        if filters.get('custom_cluster'):
            conditions.append("si.custom_cluster = %s")
            query_params.append(filters['custom_cluster'])

        if filters.get('custom_cluster_manager'):
            conditions.append("si.custom_cluster_manager = %s")
            query_params.append(filters['custom_cluster_manager'])

        if filters.get('customer_name'):
            conditions.append("si.customer_name = %s")
            query_params.append(filters['customer_name'])

        if filters.get('starting_posting_date') and filters.get('ending_posting_date'):
            conditions.append("si.posting_date BETWEEN %s AND %s")
            query_params.append(filters['starting_posting_date'])
            query_params.append(filters['ending_posting_date'])

        # If no conditions, return all results (or set to always true)
        where_clause = " AND ".join(conditions) if conditions else "1=1"

        # SQL query to fetch data from Sales Invoice and Customer tables
        query = f"""
            SELECT
                si.name,
                si.docstatus,
                si.currency,
                si.customer_name,
                si.grand_total,
                si.total_taxes_and_charges,
                si.posting_date,
                si.net_total,
                si.paid_amount,
                si.total_advance,
                si.custom_zone,
                si.custom_zonal_manager,
                si.custom_region,
                si.custom_regional_manager,
                si.custom_cluster,
                si.custom_cluster_manager,
                c.customer_type,
                c.customer_group,    
                c.custom_customer_category,
                c.custom_state,
                c.tax_category,
                c.default_currency,                
                COALESCE(si.outstanding_amount, 0.0) AS outstanding_amount,
                si.total 
            FROM
                `tabSales Invoice` si 
            LEFT JOIN `tabCustomer` c ON c.name = si.customer_name 
            WHERE {where_clause}
            ORDER BY si.posting_date DESC
        """
        
        # Execute the SQL query with the query parameters (use %s to prevent SQL injection)
        invoices = frappe.db.sql(query, tuple(query_params), as_dict=True)

        return invoices

    except Exception as e:
        # Handle any exceptions (e.g., database errors)
        print(f"Error occurred while fetching sales invoice data: {e}")
        return []

# Example usage
invoices = get_sales_invoice_data()

# Output the result
if invoices:
    for invoice in invoices:
        print(invoice)
else:
    print("No invoices found matching the filters.")

######

@frappe.whitelist(allow_guest=True)
def getInvoiceDetailsToRegionalManager():
    try:

        query = """
            SELECT DISTINCT 
                si.custom_regional_manager,
                e.personal_email,
                e.company_email,
                e.prefered_email,
                e.prefered_contact_email
            FROM `tabSales Invoice` si 
            LEFT JOIN `tabEmployee` e ON e.employee = si.custom_regional_manager
            WHERE 
                si.docstatus = 1  -- Only include confirmed (docstatus=1) invoices
                AND si.custom_regional_manager IS NOT NULL
        """
        regional_manager_details = frappe.db.sql(query, as_dict=True)

        if not regional_manager_details:
            frappe.log_error("No regional managers found in the system.", "Regional Manager Query")

        #Loop through each regional manager to filter and send emails

        for regional_manager in regional_manager_details:
            # Filter data based on custom_regional_manager
            filters = {
                'custom_regional_manager': regional_manager.custom_regional_manager
            }

            # Step 3: Fetch columns and data (replace these with actual logic)
            columns = get_columns()  
            data = get_data(filters)  

            if not data:
                frappe.log_error(f"No data found for regional manager {regional_manager.custom_regional_manager}.")
                continue  # Skip this iteration if no data is found for this manager

            # Generate Excel file from data
            excel_file = generate_excel(columns, data)  # Implement this function or logic to generate the Excel file

            # Save the file to a private folder in Frappe
            file_name = "Sales_Invoice_Report.xlsx"
            file_data = excel_file.getvalue()
            
            # Create a file record in Frappe
            file_doc = frappe.get_doc({
                "doctype": "File",
                "file_name": file_name,
                "file_url": "/private/files/" + file_name,
                "is_private": 1,
                "content": file_data
            })
            file_doc.insert(ignore_permissions=True)
            frappe.db.commit()

            file_path = file_doc.file_url

            #Determine the preferred email based on prefered_contact_email

            if regional_manager.prefered_contact_email == "Company Email":
                recipient_email = regional_manager.company_email
            elif regional_manager.prefered_contact_email == "Personal Email":
                recipient_email = regional_manager.personal_email
            else:
                recipient_email = regional_manager.prefered_email  

            if recipient_email:
                
                subject = "Sales Invoice  Report"
                message = "Please find the attached report."

                frappe.sendmail(
                    recipients=[recipient_email],
                    subject=subject,
                    message=message,
                    attachments=[{
                        "fname": file_doc.file_name,
                        "fcontent": file_data
                    }]
                )

            else:
                frappe.log_error(f"Regional manager {regional_manager.custom_regional_manager} has no valid email address.")

        return {"status": "success", "message": "Reports sent successfully to all regional managers."}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Failed to generate or send reports"))
        return {"status": "error", "message": str(e)}

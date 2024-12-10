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
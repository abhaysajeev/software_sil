import frappe
from frappe import _
from frappe.utils import get_datetime
from datetime import datetime, timedelta




@frappe.whitelist(allow_guest=True)
def get_attendance(employee_name, date):
    # Convert the selected date to datetime object for filtering
    start_datetime = get_datetime(date + " 00:00:00")
    end_datetime = get_datetime(date + " 23:59:59")

    # Query to fetch attendance records for the employee on the selected date
    query = """
        SELECT `employee`, `log_type`, `time`, `shift_start`, `shift_end`
        FROM `tabEmployee Checkin`
        WHERE `employee` = %s
        AND `time` BETWEEN %s AND %s
        ORDER BY `shift_start` ASC, `shift_end` ASC, `time` ASC
    """

    # Execute the query with the parameters
    attendance_records = frappe.db.sql(query, (employee_name, start_datetime, end_datetime), as_dict=True)

    # Initialize a variable to hold total working hours
    total_working_seconds = 0
    sessions = []  # List to hold individual sessions

    # Loop through the records and calculate total working hours
    for i in range(0, len(attendance_records) - 1, 2):
        # Check if the log types are paired as 'IN' and 'OUT'
        if attendance_records[i]['log_type'] == 'IN' and attendance_records[i+1]['log_type'] == 'OUT':
            # Extract the 'in_time' and 'out_time' from the records
            in_time = attendance_records[i]['time']
            out_time = attendance_records[i+1]['time']
            
            # Calculate the working seconds between 'IN' and 'OUT'
            working_seconds = (out_time - in_time).total_seconds()

            # Add to the total working seconds
            total_working_seconds += working_seconds

            # Convert working seconds to hours:minutes format
            working_hours = str(int(working_seconds // 3600)) + ":" + str(int((working_seconds % 3600) // 60)).zfill(2)

            # Extract the date from in_time (for date field) and time for in_time and out_time
            date_only = in_time.date()  # Extract date part from in_time
            time_only_in = in_time.strftime("%H:%M:%S")  # Extract time part from in_time
            time_only_out = out_time.strftime("%H:%M:%S")  # Extract time part from out_time

            # Create a labeled session (e.g., session 1, session 2, etc.)
            session_label = f"session {len(sessions) + 1}"

            # Add the session record (IN and OUT) to the sessions list
            sessions.append({
                session_label: {
                    "employee_name": employee_name,
                    "date": str(date_only),  # Store date as string in YYYY-MM-DD format
                    "in_time": time_only_in,  # Only time part (HH:MM:SS)
                    "out_time": time_only_out,  # Only time part (HH:MM:SS)
                    "working_hours": working_hours
                }
            })
        else:
            # If there's an "IN" without a matching "OUT", skip this session and move to the next pair
            continue

    # Convert total working seconds to hours:minutes format
    total_hours = int(total_working_seconds // 3600)
    total_minutes = int((total_working_seconds % 3600) // 60)
    
    total_working_hours = f"{total_hours}:{str(total_minutes).zfill(2)}"

    # Construct the final response JSON with labeled session records and total working hours in 'hours:minutes' format
    response = {
        "attendance_sessions": sessions,  # Nested session data with labeled sessions
        "working_hours": total_working_hours  # Total working hours for the day
    }

    return response


@frappe.whitelist(allow_guest=True)
def attendance_test():
    # Define the SQL query
    query = """
        SELECT 
            attendance_date, working_hours
        FROM 
            `tabAttendance`
        WHERE 
            employee_name = 'ALBIN S' AND 
            attendance_date BETWEEN '2024-11-18' AND '2024-11-24';
    """
    # Execute the query and fetch results
    return frappe.db.sql(query, as_dict=True)


# import frappe
# from datetime import datetime, timedelta

# @frappe.whitelist(allow_guest=True)
# def get_weekly_average(employee_name, selected_date):
#     # Convert the selected date string to a datetime object and get the date part
#     selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    
#     # Get the start of the week (Monday) and end of the week (Sunday)
#     start_of_week = selected_date - timedelta(days=selected_date.weekday())  # Monday of the week
#     end_of_week = start_of_week + timedelta(days=6)  # Sunday of the week
    
#     # Prepare the SQL query
#     query = """
#         SELECT 
#             attendance_date, working_hours
#         FROM 
#             `tabAttendance`
#         WHERE 
#             employee_name = %s AND 
#             attendance_date BETWEEN %s AND %s
#     """
    
#     # Execute the raw SQL query
#     results = frappe.db.sql(query, (employee_name, start_of_week, end_of_week), as_dict=True)
    
#     # Initialize response structure
#     response = {
#         'employee_name': employee_name,
#         'week_start_date': str(start_of_week),
#         'week_end_date': str(end_of_week)
#     }

#     # Calculate the total working hours and number of working days
#     if results:
#         total_hours = sum(record['working_hours'] for record in results)
#         number_of_working_days = len(results)
#         average_hours = total_hours / number_of_working_days if number_of_working_days > 0 else 0

#         response['total_working_hours'] = total_hours
#         response['number_of_working_days'] = number_of_working_days
#         response['weekly_average'] = average_hours
#     else:
#         response['total_working_hours'] = 0
#         response['number_of_working_days'] = 0
#         response['weekly_average'] = 0

#     # Return the response as a dictionary
#     return response

import frappe
import requests  # Use the requests library to call the external API

def get_context(context):
    context.read_only = 1  # Make the web form read-only
    context.attendance_data = get_attendance_data()

def get_attendance_data():
    # API endpoint URL
    api_url = "http://192.168.0.59:8000/api/method/software_sil.operations.employee_attendance.get_attendance"
    
    # Parameters (You can customize these based on the user or the data you need)
    params = {
        'date': '2024-11-19',  # Replace with dynamic date if needed
        'employee_name': 'ALBIN S'  # Replace with dynamic employee name if needed
    }
    
    try:
        # Making an HTTP GET request to the API
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Check if the request was successful
        
        # Parse the JSON response
        data = response.json()
        
        # Extract attendance session data and working hours
        attendance_sessions = data.get('message', {}).get('attendance_sessions', [])
        working_hours = data.get('message', {}).get('working_hours', '')
        
        # Format the attendance data as a simple list of sessions
        formatted_sessions = []
        for session in attendance_sessions:
            for key, value in session.items():
                formatted_sessions.append({
                    'session': key,
                    'in_time': value.get('in_time', ''),
                    'out_time': value.get('out_time', ''),
                    'working_hours': value.get('working_hours', '')
                })

        # Return the attendance data to the context
        return {
            'attendance_sessions': formatted_sessions,
            'total_working_hours': working_hours
        }
        
    except requests.exceptions.RequestException as e:
        # Handle request errors
        frappe.log_error(f"Error fetching attendance data: {str(e)}", 'Attendance API Error')
        return {
            'attendance_sessions': [],
            'total_working_hours': 'N/A'
        }

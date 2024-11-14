import pywin32
import datetime
import xlwings as xw

def schedule_interview_from_excel(row_number):
    """
    Schedules an interview using data from an Excel row.
pip 
    Args:
        row_number (int): The row number containing the interview details.
    """

    try:
        # Get the active sheet
        sheet = xw.Book.caller().sheets.active

        # Get interview details from Excel (adjust column indices as needed)
        subject = sheet.range(f"A{row_number}").value  # Assuming subject is in column A
        start_time_str = sheet.range(f"B{row_number}").value  # Start time as string
        duration_hours = sheet.range(f"C{row_number}").value  # Duration in hours
        required_attendees = sheet.range(f"D{row_number}").value.split(",")  # Comma-separated emails
        optional_attendees = sheet.range(f"E{row_number}").value.split(",")  # Comma-separated emails
        body = sheet.range(f"F{row_number}").value  # Optional body text
        location = sheet.range(f"G{row_number}").value  # Optional location

        # Convert start time string to datetime object
        start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
        end_time = start_time + datetime.timedelta(hours=duration_hours)

        # Create Outlook meeting request
        outlook = win32com.client.Dispatch("Outlook.Application")
        meeting = outlook.CreateItem(1)  # 1 represents meeting item

        meeting.Subject = subject
        meeting.Start = start_time.strftime("%Y-%m-%d %H:%M")
        meeting.End = end_time.strftime("%Y-%m-%d %H:%M")
        meeting.Location = location
        meeting.Body = body

        # Add required attendees
        for attendee in required_attendees:
            meeting.Recipients.Add(attendee.strip())  # Strip whitespace from email

        # Add optional attendees as CC
        for attendee in optional_attendees:
            recipient = meeting.Recipients.Add(attendee.strip())
            recipient.Type = 2  # 2 represents CC recipient

        meeting.Save()
        meeting.Send()

        # Provide feedback in Excel (optional)
        sheet.range(f"H{row_number}").value = "Sent!"

    except Exception as e:
        # Handle errors gracefully
        sheet.range(f"H{row_number}").value = f"Error: {str(e)}"
import pyodbc
from openai import AzureOpenAI

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=hassel.database.windows.net;"
    "DATABASE=sql;"
    "UID=hasse;"
    "PWD=YOUR_PASSWORD;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
)

def get_schedule(student_id, day):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT subject, start_time, end_time, room
            FROM school_schedule
            WHERE student_id = ? AND day_of_week = ?
            """,
            (student_id, day)
        )
        rows = cursor.fetchall()

    return [
        {
            "subject": r.subject,
            "time": f"{r.start_time} - {r.end_time}",
            "room": r.room
        }
        for r in rows
    ]

client = AzureOpenAI(
    api_key="YOUR_AZURE_OPENAI_KEY",
    api_version="2024-02-15-preview",
    azure_endpoint="https://hasselnot2.openai.azure.com/"
)

student_id = "S001"
day = "Monday"

schedule_data = get_schedule(student_id, day)

print("SCHEDULE FROM SQL:", schedule_data)

prompt = f"""
Student ID: {student_id}
Day: {day}

Schedule data:
{schedule_data}

Question:
What classes do I have on Monday?
"""

response = client.chat.completions.create(
    model="hasselnot2"
    messages=[
        {
            "role": "system",
            "content": (
                "You are a school scheduling assistant. "
                "Only answer using the provided schedule data."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print(response.choices[0].message.content)

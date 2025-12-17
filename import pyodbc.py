

print(response.choices[0].message.content)
from openai import OpenAI
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("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"))

# SQL connection (your existing get_schedule function)
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

student_id = "S001"
day = "Monday"
schedule_data = get_schedule(student_id, day)

# Create prompt text
prompt_text = f"""
Student ID: {student_id}
Day: {day}

Schedule data:
{schedule_data}

Question:
What classes do I have on Monday?
"""

# Call OpenAI Responses API
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": (
                "You are a school scheduling assistant. "
                "Only answer using the provided schedule data. "
                "If there are no classes, say so clearly."
            )
        },
        {
            "role": "user",
            "content": prompt_text
        }
    ]
)

print(response.choices[0].message.content)




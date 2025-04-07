import pandas as pd
import mysql.connector

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="h@rsha1545658",
    database="JEE"
)
cursor = conn.cursor()

# Load CSV
csv_file = "NIT_2024.csv"  # Change to your file
df = pd.read_csv(csv_file)

# Insert data
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO jee_cutoff (college_name, academic_program_name, seat_type, quota, gender, Closing_rank)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (row['Institute'], row['Academic Program Name'], row['Seat Type'], row['Quota'], row['Gender'], row['Closing Rank']))

conn.commit()
cursor.close()
conn.close()
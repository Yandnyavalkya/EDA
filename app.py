import streamlit as st
import sqlite3
from google import genai
import os
from dotenv import load_dotenv
load_dotenv()

# Create Gemini client
client = genai.Client(api_key=os.getenv("API_KEY"))


def get_gemini_response(question, prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{prompt[0]}\n\n{question}"
    )
    return response.text.strip()


def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute(sql)
    rows = cur.fetchall()

    conn.close()

    return rows


prompt = [
    """
You are an expert in converting English questions into SQL queries.

The SQL database contains one table named Naresh_it_employee with columns:

employee_name
employee_role
employee_salary

Example 1:
Question: How many records are present?
SQL:
SELECT COUNT(*) FROM Naresh_it_employee;

Example 2:
Question: Show all employees working in Data Science.
SQL:
SELECT * FROM Naresh_it_employee
WHERE employee_role='Data Science';

Return ONLY the SQL query.
Do not include ```sql or ``` in the response.

"""
]

st.set_page_config(page_title="SQL Query Generator")

st.title("Gemini SQL Assistant")

question = st.text_input("Ask your question")

if st.button("Submit"):

    sql_query = get_gemini_response(question, prompt)

    st.subheader("Generated SQL")
    st.code(sql_query, language="sql")

    try:
        data = read_sql_query(sql_query, "Naresh_it_employee.db")

        st.subheader("Result")

        if data:
            for row in data:
                st.write(row)
        else:
            st.success("No records found.")

    except Exception as e:
        st.error(e)
import json
import os
import sqlite3
import openai

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
assert OPENAI_API_KEY, "OPENAI_API_KEY environment variable is missing from .env"
openai.api_key = OPENAI_API_KEY

def generate_conversational_reply(sql_result, user_question):
    structure = [
        {
            "name": "generate_conversational_reply",
            "description": "Generates a conversational reply and justification based on the SQL query result and the user's question.",
            "parameters": {
                "type": "object",
                "properties": {
                    "answer": {
                        "type": "string",
                        "description": "The conversational answer to the user's question."
                    },
                    "justification": {
                        "type": "string",
                        "description": "The reasoning behind the answer."
                    },
                },
                "required": ["answer", "justification"]
            }
        }
    ]

    sql_prompt = f"""
    {sql_result}
    """

    reply = f"""
    It seems you've pasted in some SQL query results.
    """

    prompt = f"""
    GOAL: Generate a conversational reply and justification based on the SQL query result and the user's question: {user_question}
    """

    messages = [
        {"role": "user", "content": sql_prompt},
        {"role": "system", "content": reply},
        {"role": "user", "content": prompt}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=structure,
        function_call={
            "name": "generate_conversational_reply",
        })
    
    try:
        text_string = response.choices[0].message.function_call.arguments
        text_data = json.loads(text_string)
        return text_data
    
    except Exception as e:
        print(response.choices[0].message.function_call.arguments)
        print(e)
        return None

def create_sql(question, schema):
    functions = [
        {
            "name": "create_sql_query",
            "description": "Generates an SQL query from a natural language question to fulfill the user's intent.",
            "parameters": {
                "type": "object",
                "properties": {
                    "explanation": {
                        "type": "string",
                        "description": "An explanation of what we are trying to achieve with the query."
                    },
                    "query": {
                        "type": "string",
                        "description": "The SQL query to be executed to fulfill the user's intent."
                    },
                },
                "required": ["query", "explanation"]
            }
        }
    ]

    schema_prompt = f"""
    SCHEMA:
    ```
    {schema}
    ```
    """

    reply = '''
    It looks like you've provided a JSON representation of a table schema for JIRA IT Service Desk (ITSD) for the fiscal year 2023. The schema details various columns along with their data types and, in some cases, enumerations that restrict the values a column can take.
    What would you like me to do with the schema?
    '''

    prompt = f"""
    GOAL: Create an SQL query using the schema provided to answer the following question: {question}
    """

    messages = [
        {"role": "user", "content": schema_prompt},
        {"role": "system", "content": reply},
        {"role": "user", "content": prompt}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call={
            "name": "create_sql_query",
        }
    )

    try:
        text_string = response.choices[0].message.function_call.arguments
        text_data = json.loads(text_string)
        return text_data
    
    except Exception as e:
        print(response.choices[0].message.function_call.arguments)
        print(e)
        return None

schema = '''{"JIRA_ITSD_FY23_FULL":[{"Column Name":"Summary","Data Type":"TEXT"},{"Column Name":"Issue_key","Data Type":"TEXT"},{"Column Name":"Issue_id","Data Type":"REAL"},{"Column Name":"Issue_Type","Data Type":"TEXT","Enumerations":["Service Request","Purchase","Incident","Access","Change","Problem"],"Comments":"This is an enumerated field."},{"Column Name":"Status","Data Type":"TEXT","Enumerations":["Resolved","With Support","New","Procuring","With Approver","With Customer","Approved","Configuring"],"Comments":"This is an enumerated field."},{"Column Name":"Project_key","Data Type":"TEXT","Enumerations":["ITSD"],"Comments":"This is an enumerated field."},{"Column Name":"Project_name","Data Type":"TEXT","Enumerations":["IT Service Desk"],"Comments":"This is an enumerated field."},{"Column Name":"Priority","Data Type":"TEXT","Enumerations":["Low","High","Medium","Highest","Lowest","Blocker"],"Comments":"This is an enumerated field."},{"Column Name":"Resolution","Data Type":"TEXT","Enumerations":["Done","Withdrawn","Won't Do","Duplicate","Cannot Reproduce","Declined","Deferred","Rejected","Failed"],"Comments":"This is an enumerated field."},{"Column Name":"Assignee","Data Type":"TEXT"},{"Column Name":"Reporter","Data Type":"TEXT"},{"Column Name":"Creator","Data Type":"TEXT"},{"Column Name":"Created","Data Type":"TIMESTAMP"},{"Column Name":"Updated","Data Type":"TIMESTAMP"},{"Column Name":"Last_Viewed","Data Type":"TIMESTAMP"},{"Column Name":"Resolved","Data Type":"TIMESTAMP"},{"Column Name":"Component_s","Data Type":"TEXT"},{"Column Name":"Labels","Data Type":"TEXT"},{"Column Name":"Labels_1","Data Type":"TEXT"},{"Column Name":"Labels_2","Data Type":"TEXT"},{"Column Name":"Labels_3","Data Type":"TEXT","Enumerations":["Spoof","SOC-Incidents","PhishingIncident","ThirdPartyCyberIncident","NoMFAloginIncident","Spark","SuspiciousActivity","HybridSOC-Escalations"],"Comments":"This is an enumerated field."},{"Column Name":"Labels_4","Data Type":"TEXT","Enumerations":["Upguard","Spoof","PhishingIncident"],"Comments":"This is an enumerated field."},{"Column Name":"Custom_field_Access_Type","Data Type":"TEXT","Enumerations":["Contractor Extension","Contractor","AD Group"],"Comments":"This is an enumerated field."},{"Column Name":"Custom_field_Account","Data Type":"TEXT"},{"Column Name":"Custom_field_Activity","Data Type":"TEXT","Enumerations":["IT","Sales"],"Comments":"This is an enumerated field."},{"Column Name":"Custom_field_Assignment_Group","Data Type":"TEXT"},{"Column Name":"Custom_field_Business_Unit","Data Type":"TEXT","Enumerations":["Fertilisers","Shared Services","Kleenheat","Australian Vinyls","Chemicals","Decipher"],"Comments":"This is an enumerated field."},{"Column Name":"Custom_field_Category","Data Type":"TEXT","Enumerations":["User Access","Client Application","Computer","Mobile Device","Business System","Peripheral Device","Cyber Security","Server Infrastructure","Network"],"Comments":"This is an enumerated field."},{"Column Name":"Custom_field_ReporterBU","Data Type":"TEXT","Enumerations":["Company: Fertilisers, ","Company: Sodium Cyanide, ","Company: Shared Services, ","Company: Kleenheat, ","Company: Ammonia/AN, ","Company: Support Services, ","Company: Australian Vinyls, ","Company: Chemicals, ","Company: Decipher, "],"Comments":"This is an enumerated field."},{"Column Name":"Custom_field_ReporterDivision","Data Type":"TEXT"}]}'''
    
def run_sql(db_path, sql_query):
    print(f"Running SQL query: {sql_query}")
    if not sql_query.lower().startswith("select"):
        print(f"Attempted to run a non-select statement: {sql_query}")
        return None
    
    try:
        # Establishing a new connection for this method call
        conn = sqlite3.connect(db_path)
        cursor = conn.execute(sql_query)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"Error executing query: {sql_query}")
        print(e)
        return None
    

def main():
    # Step 1: Ask for user input
    question = input("What would you like to know from the database? ")

    # Step 2: Generate SQL query
    sql_data = create_sql(question, schema)
    if sql_data is None:
        print("Error generating SQL query.")
        return

    query, explanation = sql_data["query"], sql_data["explanation"]
    print(f"Generated SQL query: {query}")
    print(f"Explanation: {explanation}")

    # Step 3: Ask user if query is okay to run
    proceed = input("Is this query okay to run? (y/n) ").strip().lower()
    if proceed.lower() != "y":
        print("Aborting query.")
        return

    # Step 4: Run the query
    db_path = "./database.db"  # Assuming this is your SQLite database path
    rows = run_sql(db_path, query)
    if rows is None:
        print("Error executing SQL query.")
        return
    

    # Step 5: Generate a conversational reply
    conversational_data = generate_conversational_reply(rows, question)
    if conversational_data is None:
        print("Error generating conversational reply.")
        return
    
        # Line break in red text
    print("\033[91m" + "-" * 50 + "\033[0m")
    
    # print the sql query and the result
    print(f"SQL query: {query}")
    print()
    print(f"SQL result: {rows}")
    print("\033[91m" + "-" * 50 + "\033[0m")

    answer, justification = conversational_data["answer"], conversational_data["justification"]
    print(f"Answer: {answer}")
    print(f"Justification: {justification}")



# Assuming you've already defined `create_sql`, `run_sql`, and `generate_conversational_reply` functions
# Import or paste those functions here

if __name__ == '__main__':
    main()
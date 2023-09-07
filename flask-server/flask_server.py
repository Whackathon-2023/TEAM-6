# SQL - "I need a ticket where I was the reporter and the assignee was 'John Smith'"
# Semantic ID - "Find a me a similar ticket to [ticket_id]"
# Semantic Search - "A user can't log into the wifi. Find me a ticket that is similar to this one."

# Flask is a framework for creating a web server, using Python
# Flask - framework
# Server - Something that listens for requests and sends responses
# Python - programming language

# This server will accept:
# The Question - and will reply with a markdown response

# We import modules - these are libraries of code that we can use
from datetime import date
import json
import os
from flask import Flask, request, jsonify
import numpy as np
import openai
import sqlite3

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
assert OPENAI_API_KEY, "OPENAI_API_KEY environment variable is missing from .env"
openai.api_key = OPENAI_API_KEY

# Additional information about the schema
# Tickets are considered closed only when their status is 'Resolved.'
# Timestamps difference will return seconds
# The assignee is the person who is currently assigned to the ticket
# The reporter is the person who reported the ticket
# The creator is the person who created the ticket

# Inputs the current date using the SQLite function date('now'), in memory
today = date.today()

schema = '''
{"JIRA_ITSD_FY23_FULL":[{"Column Name":"Summary","Data Type":"TEXT"},{"Column Name":"Issue_key","Data Type":"TEXT"},{"Column Name":"Issue_id","Data Type":"REAL"},{"Column Name":"Issue_Type","Data Type":"TEXT","Enumerations":["Service Request","Purchase","Incident","Access","Change","Problem"],"Comments":"This is an enumerated field."},{"Column Name":"Status","Data Type":"TEXT","Enumerations":["Resolved","With Support","New","Procuring","With Approver","With Customer","Approved","Configuring"],"Comments":"This is an enumerated field."},{"Column Name":"Project_key","Data Type":"TEXT","Enumerations":["ITSD"],"Comments":"This is an enumerated field."},{"Column Name":"Project_name","Data Type":"TEXT","Enumerations":["IT Service Desk"],"Comments":"This is an enumerated field."},{"Column Name":"Priority","Data Type":"TEXT","Enumerations":["Low","High","Medium","Highest","Lowest","Blocker"],"Comments":"This is an enumerated field."},{"Column Name":"Resolution","Data Type":"TEXT","Enumerations":["Done","Withdrawn","Won't Do","Duplicate","Cannot Reproduce","Declined","Deferred","Rejected","Failed"],"Comments":"This is an enumerated field."},{"Column Name":"Assignee","Data Type":"TEXT"},{"Column Name":"Reporter","Data Type":"TEXT"},{"Column Name":"Creator","Data Type":"TEXT"},{"Column Name":"Created","Data Type":"TIMESTAMP"},{"Column Name":"Updated","Data Type":"TIMESTAMP"},{"Column Name":"Last_Viewed","Data Type":"TIMESTAMP"},{"Column Name":"Resolved","Data Type":"TIMESTAMP"},{"Column Name":"Component_s","Data Type":"TEXT"},{"Column Name":"Labels","Data Type":"TEXT"},{"Column Name":"Labels_1","Data Type":"TEXT"},{"Column Name":"Labels_2","Data Type":"TEXT"},{"Column Name":"Labels_3","Data Type":"TEXT","Enumerations":["Spoof","SOC-Incidents","PhishingIncident","ThirdPartyCyberIncident","NoMFAloginIncident","Spark","SuspiciousActivity","HybridSOC-Escalations"],"Comments":"This is an enumerated field."},{"Column Name":"Labels_4","Data Type":"TEXT","Enumerations":["Upguard","Spoof","PhishingIncident"],"Comments":"This is an enumerated field."},{"Column Name":"Custom_field_Access_Type","Data Type":"TEXT","Enumerations":["Contractor Extension","Contractor","AD Group"],"Comments":"This is an enumerated field."},{"Column Name":"Custom_field_Account","Data Type":"TEXT"},{"Column Name":"Custom_field_Activity","Data Type":"TEXT","Enumerations":["IT","Sales"],"Comments":"This is an enumerated field."},{"Column Name":"Custom_field_Assignment_Group","Data Type":"TEXT"},{"Column Name":"Custom_field_Business_Unit","Data Type":"TEXT","Enumerations":["Fertilisers","Shared Services","Kleenheat","Australian Vinyls","Chemicals","Decipher"],"Comments":"This is an enumerated field."},{"Column Name":"Custom_field_Category","Data Type":"TEXT","Enumerations":["User Access","Client Application","Computer","Mobile Device","Business System","Peripheral Device","Cyber Security","Server Infrastructure","Network"],"Comments":"This is an enumerated field."},{"Column Name":"Custom_field_ReporterBU","Data Type":"TEXT","Enumerations":["Company: Fertilisers, ","Company: Sodium Cyanide, ","Company: Shared Services, ","Company: Kleenheat, ","Company: Ammonia/AN, ","Company: Support Services, ","Company: Australian Vinyls, ","Company: Chemicals, ","Company: Decipher, "],"Comments":"This is an enumerated field."},{"Column Name":"Custom_field_ReporterDivision","Data Type":"TEXT"}]}
Tickets are considered closed only when their status is 'Resolved.', AVG(JULIANDAY(Resolved) - JULIANDAY(Created)) will return the average number of days it takes to resolve a ticket. The assignee is the person who is currently assigned to the ticket. The reporter is the person who reported the ticket. The creator is the person who created the ticket. 
The current date is ''' + str(today)

app = Flask(__name__)

# Loadings embeddings into memory
print("Loading embeddings into memory...")
EMBEDDINGS_FILE = "issue_description_embeddings.json"
with open(EMBEDDINGS_FILE, "r") as f:
    embeddings = json.load(f)

# Converts into a numpy array
for key in embeddings:
    embeddings[key] = np.array(embeddings[key])

print("Embeddings loaded.")

# Create a route - this is a URL that we can visit


@app.route('/question', methods=['POST'])
def question():
    # JSON is a way of representing data
    request_data = request.get_json()
    print(request_data)
    question = request_data['question']
    function, result = uhhh_like_umm_reviewing_the_question(question)
    if function == "generate_sql_for_fixed_columns":
        # In this case, we want to query the database
        print(f"SQL Query: {result['query_string']}")
        result = query_database(result['query_string'])  # Can return None
        if result is None:
            return jsonify({"content": "I don't know how to answer that question."})
        print(f"Result: {result}")
        return jsonify({"content": result})
        # Need to turn conversational / markdown
    elif function == "extract_ticket_id_for_similarity_search":
        # We want to perform an vector similarity search
        # We first get the embedding for the ticket_id, then we perform a vector similarity search
        print(f"Ticket ID: {result['ticket_id']}")
        ticket_id = result['ticket_id']
        embedding = embeddings[ticket_id]
        most_similar = get_most_similar(ticket_id, embedding, embeddings, 3)
        print(f"Most similar tickets: {most_similar}")
        result = select_tickets(most_similar)
        print(f"Result: {result}")
        return jsonify({"content": result})
        # Need to turn conversational / markdown
    elif function == "extract_description_and_find_similarity":
        # We want to perform an vector similarity search on the ticket description
        print(f"Ticket Description: {result['ticket_description']}")
        ticket_description = result['ticket_description']
        embedding = process_embedding(ticket_description)  # Can return None
        if embedding is None:
            print("I don't know how to answer that question.")
            return jsonify({"content": "I don't know how to answer that question."})
        most_similar = get_most_similar(
            ticket_description, embedding, embeddings, 3)
        print(f"Most similar tickets: {most_similar}")
        result = select_tickets(most_similar)
        print(f"Result: {result}")
        return jsonify({"content": result})
    else:
        print("I don't know how to answer that question.")
        return jsonify({"content": "I don't know how to answer that question."})

# Alana chose the name of the function
def uhhh_like_umm_reviewing_the_question(question):
    structure = [
        {
            "name": "generate_sql_for_fixed_columns",
            "description": "Generates an SQLite query based on specific columns in the database when the user query explicitly refers to columns or states.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query_string": {
                        "type": "string",
                        "description": "The generated SQLite query that will fetch the desired data based on the specific columns."
                    },
                    "explanation": {
                        "type": "string",
                        "description": "A detailed explanation for why this specific SQL query was generated."
                    }
                },
                "required": ["query_string", "explanation"]
            }
        },
        {
            "name": "extract_ticket_id_for_similarity_search",
            "description": "Identifies and extracts the ticket ID from the user's query to perform a similarity search using embeddings. Ticket ID: ITSD-******",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "string",
                        "description": "The extracted ticket ID that will be used for a similarity search."
                    },
                    "explanation": {
                        "type": "string",
                        "description": "Explanation for why the ticket ID was extracted from the user's query."
                    }
                },
                "required": ["ticket_id", "explanation"]
            }
        },
        {
            "name": "extract_description_and_find_similarity",
            "description": "Processes the user's natural language query to extract the core issue description.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_description": {
                        "type": "string",
                        "description": "The extracted issue description that forms the basis for searching similar tickets. This is a cleaned-up and normalized version of the user's query, retaining only the crucial elements that define the problem. Example: 'User can't log into the wifi on their laptop after changing their password.'"
                    },
                    "explanation": {
                        "type": "string",
                        "description": "Explanation for how the problem description was extracted and converted into an embedding."
                    }
                },
                "required": ["description_embedding", "explanation"]
            }
        }
    ]

    working_structure = [
        {
            "name": "question_to_query",
            "description": "This takes in a user's question and returns a SQLite query that get data to answer the question.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sqlite_query": {
                        "type": "string",
                        "description": "A SQLite query that will return the data needed to answer the user's question."
                    },
                    "explanation": {
                        "type": "string",
                        "description": "A detailed explanation of why the query was generated."
                    }
                },
                "required": ["sqlite_query", "explanation"]
            }
        },
        {
            "name": "extract_ticket_id",
            "description": "Ticket ID: ITSD-****** - Extracts the ticket ID from a user's question when the question is in the format 'Find me a ticket similar to [ticket_id]'",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "string",
                        "description": "The ticket ID that was extracted from the user's question. Example: ITSD-******"
                    },
                }
            }
        },
        {
            "name": "extract_ticket_description",
            "description": "Extracts the issue description from a user's query when the user is searching for tickets similar to a particular problem. The function uses natural language processing to identify the core issue from the query and disregards auxiliary words or phrases.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_description": {
                        "type": "string",
                        "description": "The extracted issue description that forms the basis for searching similar tickets. This is a cleaned-up and normalized version of the user's query, retaining only the crucial elements that define the problem. Example: 'User can't log into the wifi on their laptop after changing their password.'"
                    },
                },
                "required": ["ticket_description"]
            }
        }
    ]

    prompt = f"""
    {schema}
    
    GOAL:
    You must choose one of the functions to answer the user's question: {question}
    """

    messages = [
        {"role": "user", "content": prompt},
    ]

    response = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo-16k-0613",
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=structure,
        function_call="auto",
    )

    try:
        print(response.choices[0].message)
        text_string = response.choices[0].message.function_call.arguments
        function_name = response.choices[0].message.function_call.name
        text_data = json.loads(text_string)
        return function_name, text_data
    except Exception as e:
        print(response.choices[0].message.function_call.arguments)
        print(e)
        return None, None


DATABASE_PATH = "database.db"


def query_database(sql_query):
    # Queries our sqlite database and returns the results
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    try:
        c.execute(sql_query)
        results = c.fetchall()
        conn.close()
        return results
    except Exception as e:
        print(e)
        conn.close()
        return None

# This is a function that takes in a ticket_id and returns the most similar tickets


def get_most_similar(original_ticket_id, embedding, embeddings, n):
    # Initialize an empty list to store similarities
    similarities = []

    # Normalize the input embedding
    norm_embedding = embedding / np.linalg.norm(embedding)

    for issue_id, issue_embedding in embeddings.items():
        # Skip the original ticket
        if issue_id == original_ticket_id:
            continue

        # Normalize each stored embedding
        norm_issue_embedding = issue_embedding / \
            np.linalg.norm(issue_embedding)

        # Calculate cosine similarity
        similarity = np.dot(norm_embedding, norm_issue_embedding)

        # Append similarity and issue_id to list
        similarities.append((issue_id, similarity))

    # Sort by similarity and take the top n most similar issue_ids
    most_similar = sorted(similarities, key=lambda x: x[1], reverse=True)[:n]

    # Return just the issue IDs
    return [issue_id for issue_id, _ in most_similar]

# Improve this by not selecting all columns


def select_tickets(ticket_ids):
    results = []
    for ticket_id in ticket_ids:
        sql_query = f'SELECT * FROM JIRA_ITSD_FY23_FULL WHERE Issue_key = "{ticket_id}"'
        results.append(query_database(sql_query))
    return results


def process_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    try:
        embedding = response['data'][0]['embedding']
        return embedding
    except Exception as e:
        print(e)
        return None

if __name__ == '__main__':
    app.run(debug=True, port=5000)

"""
structure = [
        {
            "name": "question_to_query",
            "description": "This takes in a user's question and returns a SQLite query that get data to answer the question.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sqlite_query": {
                        "type": "string",
                        "description": "A SQLite query that will return the data needed to answer the user's question."
                    },
                    "explanation": {
                        "type": "string",
                        "description": "A detailed explanation of why the query was generated."
                    }
                },
                "required": ["sqlite_query", "explanation"]
            }
        },
        {
            "name": "extract_ticket_id",
            "description": "Ticket ID: ITSD-****** - Extracts the ticket ID from a user's question when the question is in the format 'Find me a ticket similar to [ticket_id]'",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "string",
                        "description": "The ticket ID that was extracted from the user's question. Example: ITSD-******"
                    },
                }
            }
        },
        {
            "name": "extract_ticket_description",
            "description": "Extracts the issue description from a user's query when the user is searching for tickets similar to a particular problem. The function uses natural language processing to identify the core issue from the query and disregards auxiliary words or phrases.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_description": {
                        "type": "string",
                        "description": "The extracted issue description that forms the basis for searching similar tickets. This is a cleaned-up and normalized version of the user's query, retaining only the crucial elements that define the problem. Example: 'User can't log into the wifi on their laptop after changing their password.'"
                    },
                },
                "required": ["ticket_description"]
            }
        }
    ]
"""

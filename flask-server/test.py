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

file_path = "booby.jpeg"

a = os.popen(f"curl --upload-file {file_path} https://free.keep.sh").read()
print(a)

# data = [('Adam Ward', 1743), ('Devin Roberts', 1713), ('Diana Jimenez', 1729), ('Erin Porter', 1743), ('Heidi Vance', 1818), ('James Sheppard', 1817), ('Joel Johnson', 1802), ('John Brown', 1735), ('John Rich', 1764), ('Kimberly House', 1782), ('Matthew Hutchinson', 1770), ('Michael Williams', 1732), ('Shannon Newman', 1743), ('Sonya Luna', 1810), ('Stephen Haney', 1763)]
# question = "Can you create a visual of how many tickets each person has resolved"
# explanation = " To create a visual of how many tickets each person has resolved, we will gather data from the 'JIRA_ITSD_FY23_FULL' table. We will filter the data to include only closed tickets with the status 'Resolved'. Then, we will group the data by the 'Assignee' column and count the number of resolved tickets for each assignee. Finally, we will create a bar chart or a table to visualize the count of resolved tickets for each person."

# def generate_matplotlib_visual(data, question,explanation):
#     structure = [
#         {
#             "name": "generate_matplotlib_visual",
#             "description": "This function creates a visual representation of data using Matplotlib. The generated visual is saved to a specified location, and the function provides a comprehensive description of what the visual represents.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "python_code": {
#                         "type": "string",
#                         "description": "This parameter should contain the complete Python code necessary for generating the visual. This includes import statements, data preparation steps, and Matplotlib commands for rendering the visual."
#                     },
#                     "file_path": {
#                         "type": "string",
#                         "description": "Indicates the absolute or relative file path where the generated visual will be saved. The path should include the filename and the extension (e.g., '/path/to/save/image.png')."
#                     },
#                     "description": {
#                         "type": "string",
#                         "description": "Provides a explanation of what the generated visual aims to represent. This should include the type of visual (e.g., bar chart, line graph), the data being visualized, and any specific insights the visual is intended to convey."
#                     }
#                 },
#                 "required": ["python_code", "file_path"]
#             }
#         }
#     ]

#     prompt = f"""
#     DATA:
#     ```{data}```
#     GOAL:
#     The purpose of the visualisation is to {explanation}. It should be a .png file saved to the current directory.
#     You are Service Genie, an IT chatbot that calls functions to help answer a users question: `{question}`
#     """

#     messages = [
#         {"role": "user", "content": prompt},
#     ]

#     response = openai.ChatCompletion.create(
#         # model="gpt-3.5-turbo-16k-0613",
#         # model="gpt-3.5-turbo-0613",
#         model="gpt-4-0613",
#         messages=messages,
#         functions=structure,
#         function_call={
#             "name": "generate_matplotlib_visual",
#         }
#     )

#     try:
#         text_string = response.choices[0].message.function_call.arguments
#         text_data = json.loads(text_string)
#         return text_data
#     except Exception as e:
#         print(response.choices[0].message.function_call.arguments)
#         print(e)
#         return None
    
# response = generate_matplotlib_visual(data, question, explanation)
# print(response)
from flask import Flask, request, jsonify

import openai

app = Flask(__name__)

# Store the last response
last_response = ""

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/send_text', methods=['POST'])
def send_text():
    global last_response
    content = request.json.get('content', '')
    last_response = response(content)
    return jsonify({"status": "success"})

@app.route('/get_response')
def get_response():
    global last_response
    return jsonify({"response": last_response})

def response(content):
    openai.api_key = "chuck your key here"
   

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who is going to help the user practice their target language by acting as a conversation partner. You will engage in conversation whilst also gently correcting spelling and grammar. The language is german"},
            {"role": "user", "content": content},
        ],
        temperature=0.5,
        max_tokens=100,
        n=1,
        stop=None,
    )

    return response['choices'][0]['message']['content']

if __name__ == '__main__':
    app.run(debug=True)

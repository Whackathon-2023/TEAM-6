const { ActivityHandler, MessageFactory } = require('botbuilder');

let fetch;
import('node-fetch').then(module => {
  fetch = module.default;
});


class ATGENIE extends ActivityHandler {
    constructor() {
        super();
        this.onMessage(async (context, next) => {
            const userText = context.activity.text;
            console.log(`User text is ${userText}`)
            const replyText = await fetchResponseFromPython(userText);
            //let replyText = 'I am working.'
            await context.sendActivity(MessageFactory.text(replyText, replyText));
            await next();
        });

        this.onMembersAdded(async (context, next) => {
            const welcomeText = 'Welcome, I am ATGenie ask me anything about service tickets';
            const membersAdded = context.activity.membersAdded;
            for (let cnt = 0; cnt < membersAdded.length; ++cnt) {
                if (membersAdded[cnt].id !== context.activity.recipient.id) {
                    await context.sendActivity(MessageFactory.text(welcomeText, welcomeText));
                }
            }
            await next();
        });
    }
}

async function fetchResponseFromPython(userText) {
    // Send text to Python server
    console.log(`Sending text to Python server: ${userText}`)
    const response = await fetch('http://127.0.0.1:5000/question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: userText })
    });

    // Fetch the response from Python server
    const data = await response.json();
    console.log(`Recieved data from flask server json data is ${data}`);
    console.log(`Response to give user is ${data.content}`)
    // data sometimes comes in weird formats like nested arrays flatten just flattens it out and .join makes it a string
    return data.content;
}

module.exports.ATGENIE = ATGENIE;

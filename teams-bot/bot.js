const { ActivityHandler, MessageFactory } = require('botbuilder');

let fetch;
import('node-fetch').then(module => {
  fetch = module.default;
});


class EchoBot extends ActivityHandler {
    constructor() {
        super();
        this.onMessage(async (context, next) => {
            const userText = context.activity.text;
            const replyText = await fetchResponseFromPython(userText);
            await context.sendActivity(MessageFactory.text(replyText, replyText));
            await next();
        });

        this.onMembersAdded(async (context, next) => {
            const welcomeText = 'yoyo wassup';
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
    await fetch('http://127.0.0.1:5000/send_text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ content: userText })
    });

    // Fetch the response from Python server
    const response = await fetch('http://127.0.0.1:5000/get_response');
    const data = await response.json();
    return data.response;
}

module.exports.EchoBot = EchoBot;

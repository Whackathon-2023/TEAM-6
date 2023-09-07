const { ActivityHandler, ActionTypes, ActivityTypes, CardFactory, MessageFactory } = require('botbuilder');


// current objective get a random image link sending to the bot

let fetch;
import('node-fetch').then(module => {
  fetch = module.default;
});

class ATGENIE extends ActivityHandler {
    constructor() {
        super();
        this.onMessage(async (context, next) => {
            const userText = context.activity.text;
            console.log(`User text is ${userText}`);

            const reply = { type: ActivityTypes.Message };
            reply.text = 'FUCK YEA SENDING PHOTOS WORKS';
            reply.attachments = [this.getInternetAttachment()];

            const typing = {
                type: 'typing',
                from: {id: 'bot-id'},
                recipient: { id: 'user-id' },
                conversation: { id: 'conversation-id' }
            }
            // make the bot start typing
            // not sure if this will work couldn't find the docs
            context.sendActivity(typing);
            // await context.sendActivity(MessageFactory.text(replyText, replyText));
            await context.sendActivity(reply);
            await next();
        });

        this.onMembersAdded(async (context, next) => {
            const welcomeText = "## Hey there, I'm service Genie\n# Here are some things I can do:\n- Find similar tickets\n- Give insights into service desk members\n- Retrieve or summarize data from old tickets\n- Send me a message to get started!";

            const membersAdded = context.activity.membersAdded;
            for (let cnt = 0; cnt < membersAdded.length; ++cnt) {
                if (membersAdded[cnt].id !== context.activity.recipient.id) {
                    await context.sendActivity(MessageFactory.text(welcomeText, welcomeText));
                }
            }                                                       
            await next();
        });



    }

    getInternetAttachment() {
        return {
            name: 'testing.png',
            contentType: 'image/png',
            contentUrl: 'https://cms.hugofox.com//resources/images/a0fea022-8ec7-4a37-b4e7-214846e7656f.jpg'
        };
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
    if(data.type == 'image'){
        // do stuff here
        console.log('Recieved an image going to send an image now')
        const img = new Image();
        // img.src = data.image;
        img.src = 'https://cms.hugofox.com//resources/images/a0fea022-8ec7-4a37-b4e7-214846e7656f.jpg';
        const formData = new FormData();
        formData.append('image', img.src);
        fetch('https://your-bot-url.com/api/messages', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer <your-bot-secret>',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            type: 'message',
            attachments: [{
            contentType: 'image/jpeg',
            contentUrl: img.src,
            name: 'image.jpg'
            }]
        })
        });
    }
    console.log(`Recieved data from flask server json data is ${data}`);
    console.log(`Text response to give user is ${data.content}`)
    return data.content;
    
    }






module.exports.ATGENIE = ATGENIE;

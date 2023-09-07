const { ActivityHandler, ActionTypes, ActivityTypes, CardFactory, MessageFactory } = require('botbuilder');

// we only send images so this can be a constant
const contentType = 'image/png';


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

            const replyText = await fetchResponseFromPython(userText);

            const reply = { type: ActivityTypes.Message };
            reply.text = replyText;
            if(replyText.url){
                reply.attachments = [this.getInternetAttachment(replyText.name, contentType, replyText.url)];
            }
            // this will be blank if theres no image if theres an image 

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

    getInternetAttachment(nameOfThing, contentType, contentUrl) {
        return {
            name: nameOfThing,
            contentType: contentType,
            contentUrl: contentUrl
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
        // send image attachment as well as make content italics and bold
        console.log('Recieved an image going to send an image now')
        
    }
    console.log(`Recieved data from flask server json data is ${data}`);
    console.log(`Text response to give user is ${data.content}`)
    return data.content;
    
    }






module.exports.ATGENIE = ATGENIE;

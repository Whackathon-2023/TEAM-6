// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

const { ActivityHandler, MessageFactory } = require('botbuilder');

let fetch;

import('node-fetch').then(module => {
  fetch = module.default;
});

const openai = new OpenAIAPI({ key: "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" }); 



class Hackathon extends ActivityHandler {
    constructor() {
        super();
        // See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.
        this.onMessage(async (context, next) => {
            const replyText =  botresponse(context.activity.text);
            await context.sendActivity(MessageFactory.text(replyText, replyText));
            // By calling next() you ensure that the next BotHandler is run.
            await next();
        });

        this.onMembersAdded(async (context, next) => {
            const membersAdded = context.activity.membersAdded;
            const welcomeText = 'Welcome to Hackathon bot, #dubsonly';
            for (let cnt = 0; cnt < membersAdded.length; ++cnt) {
                if (membersAdded[cnt].id !== context.activity.recipient.id) {
                    await context.sendActivity(MessageFactory.text(welcomeText, welcomeText));
                }
            }
            // By calling next() you ensure that the next BotHandler is run.
            await next();
        });
    }
}

async function botresponse(text){
    console.log(`recieved msg: ${text}`)
    response = await getGPT3Response(text);
    return response;

}

async function getGPT3Response(prompt) {
    const engine = "text-davinci-002"; // You can use other engines like "davinci-codex"
    const maxTokens = 100;
  
    const requestPayload = {
      prompt: prompt,
      max_tokens: maxTokens
    };
  
    const response = await openai.createCompletion({ engine, ...requestPayload });
    return response.data.choices[0].text;
  }
  
  // Example usage
  getGPT3Response("respond to this message as a rude robot who doesn't want to talk to anyone")
    .then(response => {
      console.log(response);
      return response;
    })
    .catch(error => {
      console.error(error);
    });


module.exports.Hackathon = Hackathon;

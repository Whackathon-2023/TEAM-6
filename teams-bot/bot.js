import { Configuration, OpenAIApi } from "openai";
import { ActivityHandler, MessageFactory } from 'botbuilder';

// Load dotenv
import('dotenv/config').then(() => {
  // Your dotenv variables are now loaded
});

const configuration = new Configuration({
  apiKey: process.env.OPENAI_API_KEY,
});
const openai = new OpenAIAPI(configuration);

class Hackathon extends ActivityHandler {
  constructor() {
    super();
    this.onMessage(async (context, next) => {
      const replyText = await botresponse(context.activity.text); 
      await context.sendActivity(MessageFactory.text(replyText, replyText));
      await next();
    });

    this.onMembersAdded(async (context, next) => {
      const welcomeText = 'Welcome to Hackathon bot, #dubsonly';
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

async function botresponse(text) {
  const response = await runCompletion(text);
  return response;
}

async function runCompletion(data) {
  const completion = await openai.createCompletion({
    model: 'text-davinci-003',
    prompt: data,
    max_tokens: 100,
  });
  return completion.data.choices[0].text;
}

const _Hackathon = Hackathon;
export { _Hackathon as Hackathon };

# Slack Bot for GPT Chat
Simple slack bot to connect to GPT Chat.

This project uses:
- slack-bolt for Python

# Need help or have questions?
This project is supported by [Bitovi, a DevOps consultancy](https://www.bitovi.com/devops-consulting). You can get help or ask questions on our:
- [Discord Community](https://discord.gg/J7ejFsZnJ4)
- [Twitter](https://twitter.com/bitovi)
- [LinkedIn](https://www.linkedin.com/company/bitovi)

Or, you can hire us for training, consulting, or development. Set up a free consultation.

# Inspiration

The inspiration for this project is here:
https://medium.com/@alexandre.tkint/integrate-openais-chatgpt-within-slack-a-step-by-step-approach-bea43400d311


# Steps
0. Fork this repo
1. Register an app with Slack and obtain tokens
2. Obtain AWS credentials
3. Obtain the OpenAI API key
4. Install necessary dependencies
4. Run the application
5. Test out


## Step 1: Register an app with Slack and obtain tokens
The first step in integrating ChatGPT with Slack is to register an app with Slack and obtain the Slack Bot Token and Slack App Token. To do this, follow these steps:

1. Log in to your Slack workspace
2. Go to the Slack API [website](https://api.slack.com/)
3. Click on “Create an app” and select “From scratch”
4. Give your app a name, select your Slack workspace
5. In Basic information > Add features and functionality. Click on “Permissions” and in Scopes add in Bot Token Scopes: [app_mentions:read](https://api.slack.com/scopes/app_mentions:read) ; [channels:history](https://api.slack.com/scopes/channels:history) ; [channels:read](https://api.slack.com/scopes/channels:read) ; [chat:write](https://api.slack.com/scopes/chat:write)
6. In settings, click on “Socket Mode”, enable it and give the token a name. Copy the Slack Bot App Token (starts with xapp)
7. In Basic information > Add features and functionality. Click on “Event Subscriptions” and enable it. Furthermore in “Subscribe to bot events” select “[app_mention](https://api.slack.com/events/app_mention)”. Save changes.
8. Go to the “OAuth & Permissions” section and install your app to your workspace
9. Copy the Slack Bot Token (starts with `xoxb`), you'll add it to a GitHub repo secret called `DOT_ENV`.

## Step 2: Obtain AWS credentials
Sign up for an [AWS account](https://portal.aws.amazon.com/billing/signup).

You'll need
- An access key id
- A secret access key
- (optionally) A session token

To obtain these values for an AWS IAM User, see [Getting AWS credentials for an AWS IAM user](https://www.youtube.com/watch?v=C4H81Sk8GEk)

Then add GitHub Secrets accordingly for:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

## Step 3: Obtain the OpenAI API key
The next step is to obtain the OpenAI API key. Why? Will need to connect to OpenAI’s API in order to use their GPT-3 API. If you are new to this, no problem, you’ll get 18$ for free without having to provide a credit card. To generate an API key, follow these steps:

1. Go to the OpenAI API website
2. Log in or sign up for an OpenAI account
3. Go to the [API Key section](https://platform.openai.com/account/api-keys) and create a new API key
4. Copy the API key

## Step 4: Provide Slack and OpenAI keys to the app
Create a new secret in deployment repository's GitHub Secrets called `DOT_ENV` with the following contents:
```
OPENAI_API_KEY="sk-......."
SLACK_BOT_APP_TOKEN="xapp-......."
SLACK_API_KEY="xoxb-......."
```
You can add the following variables too, if you feel the need to adjust them:
```
OPENAI_ENGINE="gpt-3.5-turbo"
OPENAI_MAX_TOKENS="1024"
OPENAI_ACK_MSG="Hello from your bot! :robot_face: \nThanks for your request, I'm on it!"
OPENAI_REPLY_MSG="Here you go: \n"
```
See OpenAI engine models (here)[https://platform.openai.com/docs/models]

## Step 5: Create a GitHub Action workflow file
`.github/workflows/deploy.yaml`
```
name: Deploy

on:
  push:
    branches: [ main ]

permissions:
  contents: read

jobs:
  EC2-Deploy:
    runs-on: ubuntu-latest
    environment:
      name: ${{ github.ref_name }}
      url: ${{ steps.deploy.outputs.vm_url }}
    steps:
    - id: deploy
      name: Deploy
      uses: bitovi/github-actions-deploy-docker-to-ec2@v0.4.6
      with:
        aws_access_key_id: ${{ secrets.AWS_ACCESS_KEY_ID}}
        aws_secret_access_key: ${{ secrets.AWS_SECRET_ACCESS_KEY}}
        aws_default_region: us-east-1

        # Provide a secret called `DOT_ENV` to append environment variables to the .env file
        dot_env: ${{ secrets.DOT_ENV }}
```

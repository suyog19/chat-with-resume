from dotenv import load_dotenv
import os
from openai import OpenAI
import gradio as gr
from agents import Agent, Runner, trace, function_tool
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
import requests

def load_dotenv_file():
    load_dotenv(override=True)

def read_text_file(file_name):
    with open(file_name, 'r') as file:
        content = file.read()
    return content

def load_resume_data():
    '''Load the CV and system instructions from text files.'''
    global cv, system_instructions
    # Read the CV and system instructions from text files
    ##############################################################################
    # Ensure that 'cv.txt' and 'instructions.txt' are present in the same directory
    # as this script or provide the correct path to these files.
    ##############################################################################
    cv = read_text_file("cv.txt")
    system_instructions = read_text_file("instructions.txt")
    #print("CV Content:")
    #print(cv)

    #print("\nSystem Instructions:")
    #print(system_instructions)


def create_chat_history(history):
    '''Iterate over the history and convert it to a string format for the chat agent.'''
    #print(history)
    chat_history = ""
    for i, (question, answer) in enumerate(history):
        if i > 0:
            chat_history += ""
        else:
            chat_history += "[\n"
        chat_history += "{"
        chat_history += f"\"role\": \"user\", "
        chat_history += f"\"content\": \"{question}\""
        chat_history += "}, "

        chat_history += "{"
        chat_history += f"\"role\": \"assistant\", "
        chat_history += f"\"content\": \"{answer}\""
        chat_history += "}\n"
        if i == len(history) - 1:
            chat_history += "]"
        else:
            chat_history += ","
    
    #print("Returning Chat History:"+chat_history.strip())
    return chat_history.strip()

@function_tool
def send_email(sub: str, body: str):
    sg = sendgrid.SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))
    from_email = Email("contact@suyogjoshi.com")
    to_email = To("suyog19@gmail.com")
    subject = sub
    content = Content("text/plain", body)
    mail = Mail(from_email, to_email, subject, content)
    
    try:
        response = sg.send(mail)
        #print(f"Email sent successfully! Status code: {response.status_code}")
    except Exception as e:
        #print(f"An error occurred while sending the email: {e}")
        pass
    
    return {"status": "success"}

@function_tool
def send_push_notification(message: str):
    '''Send a push notification using Pushover.'''
    pushover_user = os.getenv("PUSHOVER_USER")
    pushover_token = os.getenv("PUSHOVER_TOKEN")
    pushover_url = "https://api.pushover.net/1/messages.json"
    print(f"Pushing message: {message}")
    payload = {
        "user": pushover_user,
        "token": pushover_token,
        "message": message
    }
    response = requests.post(pushover_url, data=payload)
    if response.status_code == 200:
        print("Message sent successfully.")
    else:
        print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")

async def chat(message, history=[]):
    tools = [send_email, send_push_notification]
    agent = Agent(
        name="Resume Chat Agent",
        model="gpt-4.1-mini",
        instructions=system_instructions+ "\n\n" + cv + create_chat_history(history),
        tools=tools
    )
    #print("history:", history)
    result = await Runner.run(agent, message)
    #print("\n\nFinal Output:")
    #print(result.final_output)
    return result.final_output

if __name__ == "__main__":
    load_dotenv_file()
    load_resume_data()
    gr.ChatInterface(
        fn=chat,
        title="Chat with My Resume",
        description="This is AI powered chat agent. It has information about my Resume and can converse with you regarding the same."
    ).launch(share=True)
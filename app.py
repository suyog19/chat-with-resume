from dotenv import load_dotenv
import os
from openai import OpenAI
import gradio as gr
from agents import Agent, Runner, trace

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
    print("CV Content:")
    print(cv)

    print("\nSystem Instructions:")
    print(system_instructions)


def create_chat_history(history):
    '''Iterate over the history and convert it to a string format for the chat agent.'''
    chat_history = ""
    for i, (role, content) in enumerate(history):
        chat_history += f"{role}: {content}\n"
    return chat_history.strip()

async def chat(message, history=[]):
   
    agent = Agent(
        name="Resume Chat Agent",
        model="gpt-4.1-mini",
        instructions=system_instructions+ "\n\n" + cv + create_chat_history(history),
    )
    print("history:", history)
    result = await Runner.run(agent, message)
    print("\n\nFinal Output:")
    print(result.final_output)
    return result.final_output




if __name__ == "__main__":
    load_dotenv_file()
    load_resume_data()
    gr.ChatInterface(
        fn=chat,
        title="Resume Chat Agent",
        description="Chat with the Resume Chat Agent. Ask questions about the CV or the agent's instructions.",
        examples=[
            ["What is your name?"],
            ["Tell me about your experience."], 
            ["What are your skills?"],
            ["What is your education background?"],
            ["What are your hobbies?"]
        ]
    ).launch(share=True)
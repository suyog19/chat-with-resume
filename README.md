---
title: career_conversation
app_file: app.py
sdk: gradio
sdk_version: 5.37.0
---
# Chat with Resume

This project is an AI-powered chat application that allows recruiters or anyone interested to interact with Suyog Joshi's resume. The chat agent responds professionally and honestly, strictly using information from the provided resume.

## Features

- Professional chat agent powered by OpenAI GPT-4.
- Shares only information present in the resume (`cv.txt`).
- Sends push notifications when a new conversation starts.
- Can notify Suyog Joshi via email if someone wants to connect.
- Built with Gradio for an interactive web interface.
- Secure environment variable management via `.env`.
- SSL support via Gradio certificate.

## Project Structure

```
.env                      # Environment variables (API keys, etc.)
.gitignore                # Git ignore rules
app.py                    # Main application code
cv.txt                    # Suyog Joshi's resume
instructions.txt          # System instructions for the chat agent
LICENSE                   # GNU GPL v3 license
README.md                 # Project documentation
requirements.txt          # Python dependencies
.gradio/
    certificate.pem       # SSL certificate for Gradio
```

## Getting Started

### Prerequisites

- Python 3.8+
- API keys for OpenAI, SendGrid, and Pushover (set in `.env`)

### Installation

1. **Clone the repository:**
    ```sh
    git clone <repo-url>
    cd chat-with-resume
    ```

2. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up environment variables:**

    Create a `.env` file in the project root with the following content:
    ```
    OPENAI_API_KEY=your_openai_api_key
    SENDGRID_API_KEY=your_sendgrid_api_key
    PUSHOVER_USER=your_pushover_user_key
    PUSHOVER_TOKEN=your_pushover_app_token
    ```

### Running the Application

```sh
python app.py
```

The Gradio interface will launch in your browser. You can share the link if you use `share=True` in Gradio.

## Usage

- Start a conversation with the chat agent.
- The agent will answer questions using only the information in `cv.txt`.
- If you wish to connect with Suyog Joshi, provide your email address and reason; the agent will notify Suyog via email.
- Push notifications are sent when a new conversation starts.

## How It Works

- The agent uses instructions from [`instructions.txt`](instructions.txt) and resume data from [`cv.txt`](cv.txt).
- The main logic is implemented in [`app.py`](app.py), which loads the resume and instructions, manages chat history, and integrates tools for email and push notifications.
- Email notifications are sent via SendGrid, and push notifications via Pushover.
- The chat agent is powered by OpenAI GPT-4 and runs in a Gradio web interface.

## Security

- Sensitive keys and tokens are stored in `.env` and not committed to version control.
- SSL certificate for Gradio is provided in `.gradio/certificate.pem`.

## License

This project is licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE) for details.

## Author

Suyog Joshi  
[LinkedIn](https://www.linkedin.com/in/suyog-joshi/)

---

**Note:**  
- Make sure you have valid API keys for OpenAI, SendGrid, and Pushover.
- The agent will not share personal information such as mobile number, email ID, or address, as

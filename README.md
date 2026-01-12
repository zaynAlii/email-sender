# AI Email Automation Agent

This project is an AI-powered email automation system designed to generate and send
plain text, attachment-based, and visually rich HTML emails using MJML templates.

Unlike traditional email scripts, this system is built around an agent-based architecture
where decision-making, planning, and validation are handled by an AI agent, while execution
is delegated to strict, deterministic tools.

## Key Features

- Agent-based email decision system (plain, attachment, or HTML)
- MJML template generation and compilation to HTML
- Safe file and path handling using tool-driven workflows
- Automatic email template structure (src/build separation)
- Jinja2 placeholders for dynamic email content
- Explicit user confirmation before execution
- Designed for reliability, clarity, and extensibility

## Why This Project Exists

Sending HTML emails reliably is complex and error-prone.
This project solves that problem by combining:
- AI reasoning for workflow orchestration
- MJML for email compatibility
- Strict tool contracts for safety

The result is a predictable, scalable, and developer-friendly email automation system.



## Use Cases

- Automated welcome emails
- Password reset emails
- Invoice and notification emails
- Marketing and transactional email systems

## Getting Started

This project uses the OpenAI Agents SDK for agent orchestration and requires Python 3.13 to run.

To set up and run this project:

1. Clone this project from the GitHub repository: [GitHub Link](https://github.com/zaynAlii/email-sender.git)
2. Navigate to the project directory: `cd [foldername]`
3. Initialize the project with uv: `uv init`
4. Change to the source directory: `cd src`
5. Before running, rewrite the configuration file to provide your own credentials as environmental variables.
6. Run the project: `uv run main.py`

**Note on Attachments:** If you want to send an email with attachments, you must provide the absolute valid path to the attachment file. If the agent complains about an invalid path, provide the agent with a valid absolute path.

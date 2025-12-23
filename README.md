# Autonomous AI Coding Agent

An agentic AI tool built in Python that leverages the Google Gemini API to perform autonomous coding tasks. This agent can read files, write code, and execute a Python interpreter to self-correct based on real-time execution feedback.

## Key Features
* Agentic Loop: Uses a continuous feedback loop to iteratively solve complex tasks by executing code and analyzing errors.
* Tool Use (Function Calling): Maps LLM intents to local system actions like file I/O and terminal execution.
* Context Management: Maintains stateful conversation history for long-running debugging sessions.
* Secure Execution: Implements verbose logging to track every decision made by the AI.

---

## Prerequisites
Before running this project, ensure you have the following installed:
* Python 3.10+
* uv: An extremely fast Python package manager.
* Google Gemini API Key: Obtain a key from Google AI Studio.

---

## Setup & Installation

### 1. Clone the repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

### 2. Configure Environment Variables
Create a .env file in the root directory and add your API key:
GEMINI_API_KEY=your_actual_key_here

### 3. Install Dependencies
uv sync

---

## Usage

To start the agent and provide it with a task, run:
uv run main.py

### Example Task:
Once the agent is running, you can provide prompts such as:
"Search for all Python files in this directory and add a docstring to every function you find."

---

## Running Tests
To run the automated test suite and verify the agent's logic:
uv run pytest
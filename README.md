# AI Agent

This project provides a sandboxed AI coding agent capable of inspecting and modifying files within a restricted working directory. It integrates with a sample calculator application and exposes helper functions for listing files, reading content, executing Python, and writing files.

## Techniques

- **Function calling**: The agent invokes helper functions (`get_file_content`, `get_files_info`, `run_python_file`, `write_file`) to interact with the environment.
- **Sandboxing**: All file operations are constrained to a specific working directory to prevent unsafe access.
- **Environment variables**: Configuration uses `.env` to load the Gemini API key.

## LLM Model

The agent communicates with the `gemini-2.0-flash-001` model through the `google-genai` client library.

## Running
1. Clone this repository:
   ```bash
   git clone https://github.com/tamB2203579/ai-agent.git
   cd ai-agent
   ```
2. Add your own project directory inside this repo (e.g. `./calculator`)
3. Install dependencies:
   ```bash
   pip install uv
   uv pip install google-genai python-dotenv
   ```
4. Create a `.env` file with your API key:
   ```
   GEMINI_API_KEY=<your_key_here>
   ```
5. Run the agent with a prompt:
   ```bash
   python main.py "What files are in the project?"
   ```
   Use `--verbose` to see each function call.


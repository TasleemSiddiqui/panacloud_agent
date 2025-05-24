# PanaCloud Agent System

A sophisticated AI agent system built with FastAPI and OpenAI Agent SDK, using uv for dependency management. This system leverages the Gemini API to coordinate multiple specialized development agents for software project planning and execution.

## Features

- **Multi-Agent System**: Coordinates between different specialized agents:
  - Planner Agent: Project planning and task breakdown
  - DevOps Agent: Infrastructure and deployment management
  - Mobile Application Developer Agent: Mobile app development expertise
  - Agentic AI Developer Agent: AI system development
  - Website Developer Agent: Full-stack web development
  - PanaCloud Agent: Main coordinator for all specialized agents

- **Real-time Streaming**: Server-Sent Events (SSE) for real-time agent updates and responses
- **FastAPI Backend**: Modern, fast, and scalable API implementation
- **Gemini AI Integration**: Powered by Google's Gemini 2.0 Flash model
- **uv Package Manager**: Fast and reliable Python package management
- **OpenAI Agent SDK**: Robust agent framework for building AI-powered applications

## Prerequisites

- Python 3.7+
- Gemini API key
- uv package manager

## Installation

1. Install uv (if not already installed):
```bash
pip install uv
```

2. Clone the repository:
```bash
git clone <repository-url>
cd panacloud_agent
```

3. Create and activate a virtual environment using uv:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

4. Install dependencies using uv:
```bash
uv pip install -r requirements.txt
```

5. Create a `.env` file in the root directory and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

## Usage

1. Start the server:
```bash
python main.py
```

2. The server will start on `http://localhost:8000`

### API Endpoints

- `GET /`: Returns a sample response for a real estate website project
- `POST /stream`: Streams real-time updates from the agent system
  - Accepts a message parameter with the project requirements
  - Returns Server-Sent Events (SSE) with agent updates and responses

## Project Structure

- `main.py`: Main application file with FastAPI setup and agent configurations
- `agents/`: Directory containing agent-related modules
  - `Agent`: Base agent class from OpenAI Agent SDK
  - `Runner`: Agent execution system
  - `AsyncOpenAI`: Async client for API interactions
  - `OpenAIChatCompletionsModel`: Model configuration
  - `ItemHelpers`: Utility functions for message handling

## Technology Stack

- **FastAPI**: Modern web framework for building APIs
- **uv**: Next-generation Python package installer and resolver
- **OpenAI Agent SDK**: Framework for building AI agents
- **Gemini API**: Google's AI model for natural language processing
- **Server-Sent Events (SSE)**: Real-time communication protocol

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Gemini API for AI capabilities
- FastAPI for the web framework
- uv for efficient package management
- OpenAI Agent SDK for agent framework
- The open-source community for various tools and libraries used in this project

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, ItemHelpers
from agents.run import RunConfig
import asyncio

# Load environment variables
load_dotenv()

app = FastAPI()

# Initialize Gemini API key
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# Configure external client for Gemini API
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Model configuration
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Run configuration
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Agent definitions
planner_agent = Agent(
    name="Planner",
    instructions=(
        "You are a software project planner. Break down high-level requirements into detailed plans, timelines, and task assignments. "
        "Create structured development roadmaps, estimate delivery timelines, and allocate tasks to appropriate agents. "
        "Ensure project feasibility and optimal resource distribution across the development lifecycle."
    )
)

dev_ops_agent = Agent(
    name="DevOps",
    instructions=(
        "You are a DevOps engineer responsible for managing infrastructure, CI/CD pipelines, deployments, and system reliability. "
        "Automate build processes, monitor system health, and ensure secure and scalable deployments. "
        "Collaborate with developers to integrate, test, and ship features efficiently and reliably."
    )
)

# Tool definitions
dev_ops_tool = dev_ops_agent.as_tool(
    tool_name="devops",
    tool_description=(
        "Handles deployment tasks, sets up CI/CD pipelines, configures infrastructure, or monitors system performance. "
        "Use for going live or debugging build/server issues."
    )
)

planner_tool = planner_agent.as_tool(
    tool_name="planner",
    tool_description=(
        "Creates project timelines, task breakdowns, or roadmaps. Use when a goal or project idea needs structured steps."
    )
)

mobile_application_agent = Agent(
    name="Mobile Application Developer",
    instructions=(
        "You are an expert mobile application developer. Design and develop mobile apps using best practices for performance, "
        "user experience, and maintainability. Focus on Android (Kotlin/Java), iOS (Swift), or cross-platform frameworks like "
        "Flutter or React Native. Provide architectural decisions and recommend tech stacks."
    )
)

agentic_ai_agent = Agent(
    name="Agentic AI Developer",
    instructions=(
        "You are a skilled agentic AI developer. Build, orchestrate, and manage AI agents for complex multi-step reasoning tasks. "
        "Use LLMs, tools, and workflows to solve problems. Delegate tasks to Planner or DevOps tools when needed."
    ),
    tools=[dev_ops_tool, planner_tool]
)

web_agent = Agent(
    name="Website Developer",
    instructions=(
        "You are a full-stack website developer skilled in modern frontend and backend technologies. Create responsive, fast, "
        "and SEO-friendly websites using frameworks like React, Next.js, Tailwind CSS, and backend services like Node.js or Django. "
        "Focus on user-friendly designs, robust architecture, and clean code."
    )
)

panacloud_agent = Agent(
    name="PanaCloud",
    instructions=(
        "You are PanaCloud, a software company delivering optimal solutions for clients. Coordinate with specialized agents "
        "(Mobile Developer, Agentic AI Developer, Website Developer) to fulfill client requirements efficiently."
    ),
    handoffs=[mobile_application_agent, agentic_ai_agent, web_agent]
)

# Streaming generator for client response
async def stream_generator(result):
    async for event in result.stream_events():
        if event.type == "raw_response_event":
            continue
        elif event.type == "agent_updated_stream_event":
            yield f"data: Agent updated: {event.new_agent.name}\n\n"
        elif event.item.type == "tool_call_item":
            yield "data: Tool was called\n\n"
        elif event.item.type == "tool_call_output_item":
            yield f"data: Tool output: {event.item.output}\n\n"
        elif event.item.type == "message_output_item":
            message = ItemHelpers.text_message_output(event.item)
            yield f"data: Message output: {message}\n\n"
        else:
            continue
        # Ensure the stream flushes data
        await asyncio.sleep(0.01)

@app.get("/")
async def main():
    result = await Runner.run(
        panacloud_agent,
        "Create a simple website for a real estate agent with property listings, contact forms, and search functionality.",
        run_config=config
    )
    return {"output": result.final_output}

@app.post("/stream")
async def main(message: str):
    result = Runner.run_streamed(
        panacloud_agent,
        message,
        run_config=config
    )
    return StreamingResponse(
        stream_generator(result),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
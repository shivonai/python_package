# from crewai import Agent, Crew, Task
# from langchain_openai import ChatOpenAI
# from shivonai.lyra import crew_toolkit

# # Replace with your actual MCP server details
# auth_token = "KCeyMtsuklOtiJNM150wZrA4sCl9CtJd"
# base_url = "http://localhost:5000"  # Your MCP server URL

# # Get CrewAI tools
# tools = crew_toolkit(auth_token, base_url)

# # Print available tools
# print(f"Available tools: {[tool.name for tool in tools]}")

# llm = ChatOpenAI(
#             temperature=0,
#             model_name="gpt-4-turbo",
#             openai_api_key="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"
#         )

# # Create a CrewAI agent with tools
# agent = Agent(
#     role="Assistant",
#     goal="Help the user with their request",
#     backstory="You're an expert assistant with access to various tools",
#     tools=tools,
#     llm=llm
# )

# # Create a simple task
# task = Task(
#     description="what listings I have?",
#     agent=agent
# )

# # Create a crew with the agent and task
# crew = Crew(
#     agents=[agent],
#     tasks=[task],
#     verbose=True
# )

# # Run the crew
# try:
#     result = crew.kickoff()
#     print(f"Result: {result}")
# except Exception as e:
#     print(f"Error: {e}")




from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI  # or any other LLM you prefer
from shivonai.lyra import crew_toolkit
import os

os.environ["OPENAI_API_KEY"] = "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"


# Initialize an LLM
# llm = ChatOpenAI(
#             temperature=0,
#             model_name="gpt-4-turbo",
#             openai_api_key="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"
#         )

llm = ChatOpenAI(temperature=0.7, model="gpt-4")

# Get CrewAI tools
tools = crew_toolkit("KCeyMtsuklOtiJNM150wZrA4sCl9CtJd")

# Print available tools
print(f"Available tools: {[tool.name for tool in tools]}")

# Create an agent with these tools
agent = Agent(
    role="Data Analyst",
    goal="Analyze data using custom tools",
    backstory="You're an expert data analyst with access to custom tools",
    tools=tools,
    llm=llm  # Provide the LLM here
)

# Create a task - note the expected_output field
task = Task(
    description="what listings I have?",
    expected_output="A detailed report with key insights and recommendations",
    agent=agent
)

crew = Crew(
    agents=[agent],
    tasks=[task]
)

result = crew.kickoff()
print(result)
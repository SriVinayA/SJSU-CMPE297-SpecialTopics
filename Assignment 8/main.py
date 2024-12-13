import streamlit as st
from crewai import Agent, Task, Crew
import os
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

if not OPENAI_API_KEY or not SERPER_API_KEY:
    st.error("Please set both OPENAI_API_KEY and SERPER_API_KEY in the .env file.")
    st.stop()

# Set up Streamlit page
st.set_page_config(layout="wide")
st.title("AI Agents to Empower Doctors")

# User inputs
gender = st.selectbox('Select Gender', ('Male', 'Female', 'Other'))
age = st.number_input('Enter Age', min_value=0, max_value=120, value=25)
symptoms = st.text_area('Enter Symptoms', 'e.g., fever, cough, headache')
medical_history = st.text_area('Enter Medical History', 'e.g., diabetes, hypertension')

# Add controls for LLM parameters
model = st.selectbox('Select Model', ['gpt-3.5-turbo', 'gpt-4'], index=0)
temperature = st.slider('Temperature', 0.0, 1.0, 0.1)
max_tokens = st.slider('Max Tokens', 100, 8000, 2000)

# Debug mode to show chain-of-thought and token usage
debug_mode = st.checkbox('Debug Mode (Show Reasoning & Token Usage)')

# Initialize tools
search_tool = SerperDevTool(api_key=SERPER_API_KEY)
scrape_tool = ScrapeWebsiteTool()

# Initialize LLM
llm = ChatOpenAI(
    model=model,
    temperature=temperature,
    max_tokens=max_tokens,
    openai_api_key=OPENAI_API_KEY
)

# Define agents
diagnostician = Agent(
    role="Medical Diagnostician",
    goal="Analyze patient symptoms and medical history to provide a preliminary diagnosis.",
    backstory="Specializes in diagnosing conditions based on symptoms and history.",
    verbose=debug_mode,
    allow_delegation=False,
    tools=[search_tool, scrape_tool],
    llm=llm
)

treatment_advisor = Agent(
    role="Treatment Advisor",
    goal="Recommend appropriate treatment plans based on the diagnosis.",
    backstory="Specializes in creating treatment plans tailored to patient needs.",
    verbose=debug_mode,
    allow_delegation=False,
    tools=[search_tool, scrape_tool],
    llm=llm
)

# Define tasks
diagnose_task = Task(
    description=(
        "Analyze the patient's symptoms ({symptoms}) and medical history ({medical_history}). "
        "If additional information is needed, use the 'Search the internet' tool with an appropriate search query. "
        "Provide a preliminary diagnosis with a list of possible conditions."
    ),
    expected_output="A preliminary diagnosis with a list of possible conditions.",
    agent=diagnostician
)

treatment_task = Task(
    description=(
        "Based on the diagnosis, recommend appropriate treatment plans step by step. "
        "Consider the patient's medical history ({medical_history}) and current symptoms ({symptoms}). "
        "Use the 'Search the internet' or 'Read website content' tools for additional information if needed. "
        "Provide detailed treatment recommendations, including medications, lifestyle changes, and follow-up care."
    ),
    expected_output="A comprehensive treatment plan tailored to the patient's needs.",
    agent=treatment_advisor
)

# Create Crew with verbosity depending on debug mode
crew = Crew(
    agents=[diagnostician, treatment_advisor],
    tasks=[diagnose_task, treatment_task],
    verbose=debug_mode  # Enable verbose mode to potentially see chain-of-thought
)

# Button to generate recommendations
if st.button("Get Diagnosis and Treatment Plan"):
    if not symptoms.strip() or not medical_history.strip():
        st.error("Please provide both symptoms and medical history.")
    else:
        with st.spinner('Generating recommendations...'):
            result = crew.kickoff(inputs={"symptoms": symptoms, "medical_history": medical_history})

            # If debug mode is enabled, try showing reasoning steps and token usage
            # Depending on how crewai logs these, you may need to adjust attribute names.
            if debug_mode:
                st.subheader("Debug Information")

                # Token usage (if available)
                if hasattr(result, 'token_usage'):
                    usage = result.token_usage
                    st.write("**Prompt Tokens:**", usage.prompt_tokens)
                    st.write("**Completion Tokens:**", usage.completion_tokens)
                    st.write("**Total Tokens:**", usage.total_tokens)

                # Chain-of-thought or logs (if available)
                if hasattr(result, 'logs'):
                    st.subheader("Chain-of-Thought / Reasoning Steps")
                    st.write(result.logs)

                # Tool usage display (if crew logs it)
                if hasattr(result, 'tool_usage'):
                    st.subheader("Tool Usage")
                    for usage in result.tool_usage:
                        st.write(f"**Tool:** {usage.tool_name}")
                        st.write(f"**Query:** {usage.input}")
                        st.write(f"**Result:** {usage.output}")

            # Display final outputs
            tasks_output = getattr(result, 'tasks_output', [])
            for task_output in tasks_output:
                agent_role = getattr(task_output, 'agent', 'Unknown Agent')
                raw_output = getattr(task_output, 'raw', 'No output provided.')
                st.subheader(f"{agent_role}'s Response")
                st.write(raw_output)

from langchain_google_genai import ChatGoogleGenerativeAI
import os

os.environ["GOOGLE_API_KEY"] = "GOOGLE_API_KEY"
llm = ChatGoogleGenerativeAI(model = "gemini-1.5-flash",temperature=0)
from crewai import Agent, Task, Crew

from crewai_tools import SerperDevTool,tool 
import os

os.environ["SERPER_API_KEY"] = "serper_api_key"
internet_search_tool = SerperDevTool()

from crewai_tools import SerperDevTool, tool
import os
import random

# Set up the Serper API key
os.environ["SERPER_API_KEY"] = "serper_api_key"
internet_search_tool = SerperDevTool()

@tool("get remedies")
def get_remedies(symptom: str) -> str:
    """
    Tool definition to search for remedies for the given symptom.
    """
    search_queries = [
        f"site:mayoclinic.org remedies for {symptom}",
        f"site:webmd.com remedies for {symptom}",
        f"site:cdc.gov preventive measures for {symptom}",
        f"site:nih.gov remedies for {symptom}",
        f"site:medlineplus.gov remedies for {symptom}",
        f"site:who.int preventive measures for {symptom}"
    ]
    
    search_queries = [random.choice(search_queries)]
    results = []
    for query in search_queries:
        search_result = internet_search_tool._run(search_query=query)
        if search_result:
            results.append(search_result)
    
    # Combine and return the search results
    combined_results = "\n\n".join(results)
    return combined_results

# Define the agent
remedies_agent = Agent(
    role="Remedies Agent",
    goal="To recommend temporary remedies for the user's symptoms before their appointment is scheduled.",
    backstory="A knowledgeable agent that provides temporary relief suggestions based on reputable sources.",
    llm=llm,
    allow_delegation=False,
    verbose=True
)

# Define the task
remedies_task = Task(
    description=(
        "1. Identify the user's symptoms from the provided information: {general_information} and {visual_information}.\n"
        "2. Search for temporary remedies using reputable sites: Mayo Clinic, WebMD, CDC, NIH, MedlinePlus, WHO  and make sure that you search for the remedies of symptoms only.\n"
        "3. When you use internet search make sure that you mention the reputable sites in the search query to get knowledge on which we can rely on.\n"
        "4. Provide a list of recommended temporary remedies for the user's symptoms in plain text."
        "5. Each remedy should be separated by a new line."
    ),
    expected_output="List of recommended temporary remedies for the user's symptoms.",
    agent=remedies_agent,
    tools=[internet_search_tool]
)

# Integrate the remedies agent and task into the crew
crew = Crew(
    agents=[ remedies_agent],
    tasks=[remedies_task],
    verbose=2
)


give_polite_message = Agent(
    role = "To give personalized motivating messages and recommendations to a person",
    goal = "To give personalized motivating messages and recommendations to a person",
    backstory = "You are a virtual assitant that is designed to give personalized motivating messages and recommendations to a person based on the recommendations given and general data about patient. You are designed to be polite and respectful to the person you are interacting with.",
    llm = llm,
    allow_delegation = False
)

giving_polite_message = Task(
    description = (
        "1. You have recommendations: {recommendation} for a person "
        "2. You have general data about the person: {general_data} "
        "3. Based on the create personalized motivating messages and recommendations for the person."
        "4. Make the message like it is a personal message from a friend."
    ),
    agent = give_polite_message,
    expected_output = "Personalized motivating messages and recommendations for the person in a conversational manner from a friend."
)

new_crew = Crew(agents=[give_polite_message], tasks=[giving_polite_message],verbose=True)

def get_polite_message(vision_information: str, general_information: str) -> str:
    """
    Function to generate a personalized motivating message for a person based on the given recommendation and general data.
    """
    # Run the crew to generate the personalized message
    inputs = {
        "general_information": general_information,
        "visual_information": vision_information
    }
    results = crew.kickoff(inputs)
    recommendation = results
    general_data = general_information
    inputs = {
    "recommendation": recommendation,
    "general_data": general_data}
    results = new_crew.kickoff(inputs)
    return results
    

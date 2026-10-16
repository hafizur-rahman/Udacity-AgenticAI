# TODO: 1 - Import the AugmentedPromptAgent class
from workflow_agents.base_agents import AugmentedPromptAgent

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = "What is the capital of France?"
persona = "You are a college professor; your answers always start with: 'Dear students,'"

# TODO: 2 - Instantiate an object of AugmentedPromptAgent with the required parameters
augmented_agent = AugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona
)
# TODO: 3 - Send the 'prompt' to the agent and store the response in a variable named 'augmented_agent_response'
augmented_agent_response = augmented_agent.respond(prompt)

# Print the agent's response
print(augmented_agent_response)

# TODO: 4 - Add a comment explaining:
# - What knowledge the agent likely used to answer the prompt.
# - How the system prompt specifying the persona affected the agent's response.

# The agent likely used its inherent knowledge about the capital of France, which is Paris, to answer the prompt. The system prompt specifying the persona as a college professor influenced the agent's response by making it more formal and structured, starting with "Dear students," as instructed in the persona description. This likely led to a response that not only provided the correct answer but also did so in a way that mimics how a college professor would address their students.
# The agent's response was generated using the AugmentedPromptAgent, which allows it to utilize its inherent knowledge while also adhering to the specified persona, resulting in a response that is both informative and stylistically consistent with the role of a college professor.
# The AugmentedPromptAgent is designed to combine the agent's inherent knowledge with the constraints and style defined in the system prompt, enabling it to generate responses that are both accurate and contextually appropriate based on the given persona.
# In this case, the agent's inherent knowledge about the capital of France was used to provide the correct answer, while the system prompt influenced the tone and structure of the response, making it more formal and aligned with the persona of a college professor.
# The response demonstrates how the AugmentedPromptAgent can effectively integrate its knowledge with the persona defined in the system prompt to produce a response that is both accurate and stylistically consistent with the specified role.

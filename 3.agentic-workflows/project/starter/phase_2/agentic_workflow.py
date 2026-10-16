# agentic_workflow.py
import sys, os

cur_dir=os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(cur_dir, '..')))

# TODO: 1 - Import the following agents: ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent from the workflow_agents.base_agents module
from phase_1.workflow_agents.base_agents import ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent

import os
from dotenv import load_dotenv

# TODO: 2 - Load the OpenAI key into a variable called openai_api_key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# load the product spec
# TODO: 3 - Load the product spec document Product-Spec-Email-Router.txt into a variable called product_spec
with open(f"{cur_dir}/Product-Spec-Email-Router.txt", "r") as f:
    product_spec = f.read()

# Instantiate all the agents

# Action Planning Agent
knowledge_action_planning = (
    "A complete product plan for the Email Router is composed of exactly three "
    "high-level steps, produced in this order:\n"
    "Step 1: Generate the user stories for the Email Router product.\n"
    "Step 2: Generate the product features for the Email Router product, grouped "
    "from the user stories.\n"
    "Step 3: Generate the engineering tasks for the Email Router product, "
    "derived from the user stories.\n"
    "When asked to plan the Email Router product, return ONLY these three short "
    "high-level steps as a numbered list. Do NOT include the actual user stories, "
    "feature descriptions, or task details inside the plan. Do NOT add sub-steps. "
    "Each step must be a single short sentence describing what to produce."
)
# TODO: 4 - Instantiate an action_planning_agent using the 'knowledge_action_planning'
action_planning_agent = ActionPlanningAgent(
    openai_api_key=openai_api_key,
    knowledge=knowledge_action_planning
)

# Product Manager - Knowledge Augmented Prompt Agent
persona_product_manager = "You are a Product Manager, you are responsible for defining the user stories for a product."
knowledge_product_manager = (
    "Stories are defined by writing sentences with a persona, an action, and a desired outcome. "
    "The sentences always start with: As a "
    "Write several stories for the product spec below, where the personas are the different users of the product. ",
    product_spec
)
# TODO: 6 - Instantiate a product_manager_knowledge_agent using 'persona_product_manager' and the completed 'knowledge_product_manager'
product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona_product_manager,
    knowledge=knowledge_product_manager
)


# Product Manager - Evaluation Agent
# TODO: 7 - Define the persona and evaluation criteria for a Product Manager evaluation agent and instantiate it as product_manager_evaluation_agent. This agent will evaluate the product_manager_knowledge_agent.
# The evaluation_criteria should specify the expected structure for user stories (e.g., "As a [type of user], I want [an action or feature] so that [benefit/value].").
persona = "You are an evaluation agent that checks the answers of other worker agents."
evaluation_criteria = "The answer should be user stories that follow this exact structure: As a [type of user], I want [an action or feature] so that [benefit/value]."
product_manager_evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=persona,
    evaluation_criteria=evaluation_criteria,
    worker_agent=product_manager_knowledge_agent,
    max_interactions=3
)

# Program Manager - Knowledge Augmented Prompt Agent
persona_program_manager = "You are a Program Manager, you are responsible for defining the features for a product."
knowledge_program_manager = "Features of a product are defined by organizing similar user stories into cohesive groups."
# Instantiate a program_manager_knowledge_agent using 'persona_program_manager' and 'knowledge_program_manager'
# (This is a necessary step before TODO 8. Students should add the instantiation code here.)
program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona_program_manager,
    knowledge=knowledge_program_manager
)

# Program Manager - Evaluation Agent
persona_program_manager_eval = "You are an evaluation agent that checks the answers of other worker agents."

# TODO: 8 - Instantiate a program_manager_evaluation_agent using 'persona_program_manager_eval' and the evaluation criteria below.
#                      "The answer should be product features that follow the following structure: " \
#                      "Feature Name: A clear, concise title that identifies the capability\n" \
#                      "Description: A brief explanation of what the feature does and its purpose\n" \
#                      "Key Functionality: The specific capabilities or actions the feature provides\n" \
#                      "User Benefit: How this feature creates value for the user"
# For the 'agent_to_evaluate' parameter, refer to the provided solution code's pattern.
program_manager_evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=persona_program_manager_eval,
    evaluation_criteria="The answer should be product features that follow the following structure: " \
                        "Feature Name: A clear, concise title that identifies the capability\n" \
                        "Description: A brief explanation of what the feature does and its purpose\n" \
                        "Key Functionality: The specific capabilities or actions the feature provides\n" \
                        "User Benefit: How this feature creates value for the user",
    worker_agent=program_manager_knowledge_agent,
    max_interactions=3
)

# Development Engineer - Knowledge Augmented Prompt Agent
persona_dev_engineer = "You are a Development Engineer, you are responsible for defining the development tasks for a product."
knowledge_dev_engineer = (
    "Development tasks are defined by identifying what needs to be built to implement each user story.",
    "Use the product spec and generated user stories to produce implementation tasks. "
    f"{product_spec}"
)

# Instantiate a development_engineer_knowledge_agent using 'persona_dev_engineer' and 'knowledge_dev_engineer'
# (This is a necessary step before TODO 9. Students should add the instantiation code here.)
development_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona_dev_engineer,
    knowledge=knowledge_dev_engineer
)

# Development Engineer - Evaluation Agent
persona_dev_engineer_eval = "You are an evaluation agent that checks the answers of other worker agents."
# TODO: 9 - Instantiate a development_engineer_evaluation_agent using 'persona_dev_engineer_eval' and the evaluation criteria below.
#                      "The answer should be tasks following this exact structure: " \
#                      "Task ID: A unique identifier for tracking purposes\n" \
#                      "Task Title: Brief description of the specific development work\n" \
#                      "Related User Story: Reference to the parent user story\n" \
#                      "Description: Detailed explanation of the technical work required\n" \
#                      "Acceptance Criteria: Specific requirements that must be met for completion\n" \
#                      "Estimated Effort: Time or complexity estimation\n" \
#                      "Dependencies: Any tasks that must be completed first"
# For the 'agent_to_evaluate' parameter, refer to the provided solution code's pattern.
development_engineer_evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=persona_dev_engineer_eval,
    evaluation_criteria="The answer should be tasks following this exact structure: " \
                        "Task ID: A unique identifier for tracking purposes\n" \
                        "Task Title: Brief description of the specific development work\n" \
                        "Related User Story: Reference to the parent user story\n" \
                        "Description: Detailed explanation of the technical work required\n" \
                        "Acceptance Criteria: Specific requirements that must be met for completion\n" \
                        "Estimated Effort: Time or complexity estimation\n" \
                        "Dependencies: Any tasks that must be completed first",
    worker_agent=development_engineer_knowledge_agent,
    max_interactions=3
)


# Routing Agent
# TODO: 10 - Instantiate a routing_agent. You will need to define a list of agent dictionaries (routes) for Product Manager, Program Manager, and Development Engineer. Each dictionary should contain 'name', 'description', and 'func' (linking to a support function). Assign this list to the routing_agent's 'agents' attribute.
routing_agent = RoutingAgent(openai_api_key, agents=[
    {
        "name": "product manager agent",
        "description": (
            "Use the Product Manager route to write user stories for the Email Router product. "
            "The Product Manager only produces user stories in the agile format "
            "'As a [type of user], I want [an action or feature] so that [benefit/value].' "
            "Choose this route whenever the step asks to identify, list, define, draft, "
            "review, or generate user stories, personas, user needs, or user-centered "
            "requirements. Do NOT choose this route for product features or engineering tasks."
        ),
        "func": lambda x: product_manager_knowledge_agent.respond(x)
    },
    {
        "name": "program manager agent",
        "description": (
            "Use the Program Manager route to define product features for the Email Router. "
            "The Program Manager groups related user stories into product features written "
            "with the labels 'Feature Name:', 'Description:', 'Key Functionality:', and "
            "'User Benefit:'. Choose this route whenever the step asks to define, list, "
            "group, organize, or generate product features, capabilities, or feature sets. "
            "Do NOT choose this route for user stories or engineering tasks."
        ),
        "func": lambda x: program_manager_knowledge_agent.respond(x)
    },
    {
        "name": "development engineer agent",
        "description": (
            "Use the Development Engineer route to define engineering tasks for the Email Router. "
            "The Development Engineer writes implementation tasks for each user story using the "
            "labels 'Task ID:', 'Task Title:', 'Related User Story:', 'Description:', "
            "'Acceptance Criteria:', 'Estimated Effort:', and 'Dependencies:'. Choose this "
            "route whenever the step asks to define, break down, or generate engineering tasks, "
            "development tasks, implementation tasks, technical work items, or backlog tasks. "
            "Do NOT choose this route for user stories or product features."
        ),
        "func": lambda x: development_engineer_knowledge_agent.respond(x)
    }
])

# Job function persona support functions
# TODO: 11 - Define the support functions for the routes of the routing agent (e.g., product_manager_support_function, program_manager_support_function, development_engineer_support_function).
# Each support function should:
#   1. Take the input query (e.g., a step from the action plan).
#   2. Get a response from the respective Knowledge Augmented Prompt Agent.
#   3. Have the response evaluated by the corresponding Evaluation Agent.
#   4. Return the final validated response.

def product_manager_support_function(query):
    response = product_manager_knowledge_agent.respond(query)
    evaluation = product_manager_evaluation_agent.evaluate(query, response)
    return response if "acceptable" in evaluation.lower() else f"Product Manager Agent's response did not meet the criteria: {evaluation}"  

def program_manager_support_function(query):
    response = program_manager_knowledge_agent.respond(query)
    evaluation = program_manager_evaluation_agent.evaluate(query, response)
    return response if "acceptable" in evaluation.lower() else f"Program Manager Agent's response did not meet the criteria: {evaluation}"  

def development_engineer_support_function(query):
    response = development_engineer_knowledge_agent.respond(query)
    evaluation = development_engineer_evaluation_agent.evaluate(query, response)
    return response if "acceptable" in evaluation.lower() else f"Development Engineer Agent's response did not meet the criteria: {evaluation}"  

# Run the workflow

print("\n*** Workflow execution started ***\n")
# Workflow Prompt
# ****
#workflow_prompt = "What would the development tasks for this product be?"
workflow_prompt = (
    "Build a comprehensive product plan for the Email Router product. "
    "The plan must produce user stories, then product features, then engineering "
    "tasks. Return only the high-level steps required to deliver this plan."
)
# ****
print(f"Task to complete in this workflow, workflow prompt = {workflow_prompt}")

print("\nDefining workflow steps from the workflow prompt")
# TODO: 12 - Implement the workflow.
#   1. Use the 'action_planning_agent' to extract steps from the 'workflow_prompt'.
#   2. Initialize an empty list to store 'completed_steps'.
#   3. Loop through the extracted workflow steps:
#      a. For each step, use the 'routing_agent' to route the step to the appropriate support function.
#      b. Append the result to 'completed_steps'.
#      c. Print information about the step being executed and its result.
#   4. After the loop, print the final output of the workflow (the last completed step).
# Step 1: Extract steps from the workflow prompt using the action_planning_agent
extracted_steps = action_planning_agent.extract_steps_from_prompt(workflow_prompt)
print(f"Extracted workflow steps: {extracted_steps}")

# Step 2: Initialize an empty list to store completed steps
completed_steps = []
# Step 3: Loop through the extracted workflow steps
for step in extracted_steps:
    step = step.strip()
    if not step:
        continue
    print(f"\nExecuting step: {step}")
    
    # Step 3a: Use the routing_agent to route the step to the appropriate support function
    result = routing_agent.route(step)
    
    # Step 3b: Append the result to completed_steps
    completed_steps.append(result)
    
    # Step 3c: Print information about the step being executed and its result
    print(f"Result of executing step: {result}")

# Step 4: Print the final output of the workflow (the last completed step)
print(f"\nFinal output of the workflow: {completed_steps[-1] if completed_steps else 'No steps completed'}")

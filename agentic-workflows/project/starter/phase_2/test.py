#!/usr/bin/env python3
"""
Test script to validate that the agentic workflow produces outputs
that follow the exact structures required by the evaluation criteria.
"""

import sys
import os
import re

# Add the phase_1 directory to the path to import workflow_agents
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'phase_1'))

from workflow_agents.base_agents import (
    ActionPlanningAgent,
    KnowledgeAugmentedPromptAgent,
    EvaluationAgent,
)

from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    print("OPENAI_API_KEY not found in environment variables")
    sys.exit(1)

# Load the product spec
product_spec_path = os.path.join(os.path.dirname(__file__), "Product-Spec-Email-Router.txt")
with open(product_spec_path, "r", encoding="utf-8") as f:
    product_spec = f.read()

def test_user_stories_structure():
    """Test that user stories follow the exact required structure."""
    print("=== Testing User Stories Structure ===")
    
    persona_product_manager = "You are a Product Manager, you are responsible for defining the user stories for a product."
    knowledge_product_manager = (
        "You must create user stories that follow this EXACT structure: 'As a [type of user], I want [an action or feature] so that [benefit/value].'\n"
        "Each user story must be a complete sentence starting with 'As a' and ending with a clear benefit.\n"
        "Identify different user personas from the product specification and create multiple user stories.\n"
        "Each user story should represent a specific functionality or feature mentioned in the specification.\n"
        "Write each user story on a separate line.\n"
        f"\n\nProduct Specification:\n{product_spec}"
    )
    
    product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(
        persona=persona_product_manager,
        knowledge=knowledge_product_manager,
        openai_api_key=openai_api_key,
    )
    
    evaluation_criteria_product_manager = (
        "The answer MUST be user stories that follow this EXACT structure: 'As a [type of user], I want [an action or feature] so that [benefit/value].'\n"
        "Each user story must:\n"
        "- Start with 'As a' followed by a user type\n"
        "- Include 'I want' followed by a specific action or feature\n"
        "- End with 'so that' followed by a clear benefit or value\n"
        "- Be a complete, grammatically correct sentence\n"
        "- Represent a specific functionality from the product specification\n"
        "If the response does not follow this exact format, provide specific correction instructions."
    )
    
    prompt = "Create user stories for the Email Router product based on the specification."
    
    product_manager_evaluation_agent = EvaluationAgent(
        persona=persona_product_manager,
        worker_agent=product_manager_knowledge_agent,
        max_interactions=5,
        openai_api_key=openai_api_key,
        evaluation_criteria=evaluation_criteria_product_manager
    )
    
    result = product_manager_evaluation_agent.evaluate(
        initial_prompt=prompt
    )

    
    print("User Stories Result:")
    print(result["final_response"])
    print(f"Evaluation: {result['evaluation']}")
    print(f"Interactions: {result['interactions']}")
    
    # Validate structure
    user_stories = result["final_response"].split('\n')
    valid_stories = 0
    
    for story in user_stories:
        story = story.strip()
        if story and story.startswith("As a") and "I want" in story and "so that" in story:
            valid_stories += 1
            print(f"✅ Valid story: {story}")
        elif story:
            print(f"❌ Invalid story: {story}")
    
    print(f"\nValid stories: {valid_stories}/{len([s for s in user_stories if s.strip()])}")
    return valid_stories > 0

def test_product_features_structure():
    """Test that product features follow the exact required structure."""
    print("\n=== Testing Product Features Structure ===")
    
    persona_program_manager = "You are a Program Manager, you are responsible for defining the features for a product."
    knowledge_program_manager = (
        "You must create product features that follow this EXACT structure:\n"
        "Feature Name: [A clear, concise title that identifies the capability]\n"
        "Description: [A brief explanation of what the feature does and its purpose]\n"
        "Key Functionality: [The specific capabilities or actions the feature provides]\n"
        "User Benefit: [How this feature creates value for the user]\n\n"
        "Group related user stories into cohesive features.\n"
        "Each feature should represent a major capability of the product.\n"
        "Provide clear, specific details for each section.\n"
        "Separate each feature with a blank line."
    )
    
    program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(
        persona=persona_program_manager,
        knowledge=knowledge_program_manager,
        openai_api_key=openai_api_key,
    )
    
    evaluation_criteria_program_manager = (
        "The answer MUST be product features that follow this EXACT structure:\n"
        "Feature Name: [A clear, concise title that identifies the capability]\n"
        "Description: [A brief explanation of what the feature does and its purpose]\n"
        "Key Functionality: [The specific capabilities or actions the feature provides]\n"
        "User Benefit: [How this feature creates value for the user]\n\n"
        "Each feature must:\n"
        "- Have a clear, descriptive Feature Name\n"
        "- Include a detailed Description explaining the feature's purpose\n"
        "- List specific Key Functionality items\n"
        "- Explain clear User Benefits\n"
        "- Be separated from other features with blank lines\n"
        "If the response does not follow this exact format, provide specific correction instructions."
    )
    
    program_manager_evaluation_agent = EvaluationAgent(
        persona=persona_program_manager,
        worker_agent=program_manager_knowledge_agent,
        max_interactions=5,
        openai_api_key=openai_api_key,
        evaluation_criteria=evaluation_criteria_program_manager,
    )
    
    prompt = "Create product features for the Email Router product based on the specification."
    result = program_manager_evaluation_agent.evaluate(
        initial_prompt=prompt
    )
    
    print("Product Features Result:")
    print(result["final_response"])
    print(f"Evaluation: {result['evaluation']}")
    print(f"Interactions: {result['interactions']}")
    
    # Validate structure
    features = result["final_response"].split('\n\n')
    valid_features = 0
    
    for feature in features:
        if "Feature Name:" in feature and "Description:" in feature and "Key Functionality:" in feature and "User Benefit:" in feature:
            valid_features += 1
            print(f"✅ Valid feature structure found")
        elif feature.strip():
            print(f"❌ Invalid feature structure")
    
    print(f"\nValid features: {valid_features}/{len([f for f in features if f.strip()])}")
    return valid_features > 0

def test_engineering_tasks_structure():
    """Test that engineering tasks follow the exact required structure."""
    print("\n=== Testing Engineering Tasks Structure ===")
    
    persona_dev_engineer = "You are a Development Engineer, you are responsible for defining the development tasks for a product."
    knowledge_dev_engineer = (
        "You must create development tasks that follow this EXACT structure:\n"
        "Task ID: [A unique identifier for tracking purposes]\n"
        "Task Title: [Brief description of the specific development work]\n"
        "Related User Story: [Reference to the parent user story]\n"
        "Description: [Detailed explanation of the technical work required]\n"
        "Acceptance Criteria: [Specific requirements that must be met for completion]\n"
        "Estimated Effort: [Time or complexity estimation]\n"
        "Dependencies: [Any tasks that must be completed first]\n\n"
        "Create detailed engineering tasks for implementing the product features.\n"
        "Each task should be specific and actionable.\n"
        "Provide realistic effort estimates and identify dependencies.\n"
        "Separate each task with a blank line."
    )
    
    development_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(
        persona=persona_dev_engineer,
        knowledge=knowledge_dev_engineer,
        openai_api_key=openai_api_key,
    )
    
    evaluation_criteria_dev_engineer = (
        "The answer MUST be tasks following this EXACT structure:\n"
        "Task ID: [A unique identifier for tracking purposes]\n"
        "Task Title: [Brief description of the specific development work]\n"
        "Related User Story: [Reference to the parent user story]\n"
        "Description: [Detailed explanation of the technical work required]\n"
        "Acceptance Criteria: [Specific requirements that must be met for completion]\n"
        "Estimated Effort: [Time or complexity estimation]\n"
        "Dependencies: [Any tasks that must be completed first]\n\n"
        "Each task must:\n"
        "- Have a unique Task ID (e.g., T001, T002, etc.)\n"
        "- Include a clear Task Title\n"
        "- Reference a Related User Story\n"
        "- Provide detailed Description of technical work\n"
        "- List specific Acceptance Criteria\n"
        "- Include realistic Estimated Effort\n"
        "- Identify Dependencies if any\n"
        "- Be separated from other tasks with blank lines\n"
        "If the response does not follow this exact format, provide specific correction instructions."
    )
    
    development_engineer_evaluation_agent = EvaluationAgent(
        persona=persona_dev_engineer,
        worker_agent=development_engineer_knowledge_agent,
        max_interactions=5,
        openai_api_key=openai_api_key,
        evaluation_criteria=evaluation_criteria_dev_engineer
    )
    
    prompt = "Create engineering tasks for the Email Router product implementation."
    result = development_engineer_evaluation_agent.evaluate(
        initial_prompt=prompt
    )
    
    print("Engineering Tasks Result:")
    print(result["final_response"])
    print(f"Evaluation: {result['evaluation']}")
    print(f"Interactions: {result['interactions']}")
    
    # Validate structure
    tasks = result["final_response"].split('\n\n')
    valid_tasks = 0
    
    for task in tasks:
        if all(keyword in task for keyword in ["Task ID:", "Task Title:", "Related User Story:", "Description:", "Acceptance Criteria:", "Estimated Effort:", "Dependencies:"]):
            valid_tasks += 1
            print(f"✅ Valid task structure found")
        elif task.strip():
            print(f"❌ Invalid task structure")
    
    print(f"\nValid tasks: {valid_tasks}/{len([t for t in tasks if t.strip()])}")
    return valid_tasks > 0

def main():
    """Run all structure validation tests."""
    print("Starting structured output validation tests...")
    print("=" * 60)
    
    results = []
    
    # Test user stories structure
    results.append(test_user_stories_structure())
    
    # Test product features structure  
    results.append(test_product_features_structure())
    
    # Test engineering tasks structure
    results.append(test_engineering_tasks_structure())
    
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(f"User Stories Structure: {'✅ PASS' if results[0] else '❌ FAIL'}")
    print(f"Product Features Structure: {'✅ PASS' if results[1] else '❌ FAIL'}")
    print(f"Engineering Tasks Structure: {'✅ PASS' if results[2] else '❌ FAIL'}")
    
    all_passed = all(results)
    print(f"\nOverall Result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    return all_passed

if __name__ == "__main__":
    main()
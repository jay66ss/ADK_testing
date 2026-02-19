"""
Model configuration demonstration showing factual vs creative optimization.
Demonstrates ADK's generate_content_config with different settings.
"""
from google.adk.agents import LlmAgent
from google.genai import types




# Agent 1: Optimized for Factual Data Extraction
# Uses low temperature for consistency, strict safety for accuracy
factual_agent = LlmAgent(
    model = "gemini-2.5-flash",
    name = "data_extractor",
    description = "Extracts factual information with high accuracy and consistency",
    instruction = """You are a precise data extractor.
    Extract facts exactly as stated. Do not: 
    - Add information not present in the input
    - Make assumptions or inferences
    - Use creative language or embellishments
    Be accurate, concise and deterministic.""",
    generate_content_config = types.GenerateContentConfig(
        temperature = 0.1,  # Low temperature for deterministic output
        max_output_tokens = 500,  # Limit output length for concise responses
        safety_settings = [
            types.SafetySetting(
                category = types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold = types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
            )   
        ]
    )
)
# Agent 2: Optimized for Creative Content Generation
# Uses high temperature for creativity, Pro model for better ideas
creative_agent = LlmAgent(
    model = "gemini-2.5-flash",
    name = "creative_brainstormer",
    description = "Generates creative content with rich language and ideas",
    instruction = """You are a creative brainstorming partner.
    Generate innovative, diverse and imaginative ideas. Feel free to:
    - Think outside the box
    - Combine unexpected concepts
    - Explore unconventional approaches
    Be creative, varied, and thought-provoking.
    """,
    generate_content_config = types.GenerateContentConfig(
        temperature = 0.9,  # High temperature for creative output
        max_output_tokens = 2000,  # Allow longer responses for richer content
        top_p=0.95,
        top_k=40,
        
        safety_settings = [
            types.SafetySetting(
                category = types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold = types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
            )   
        ]
    )
)
# For adk web, we'll use the factual agent as root agent. Switch to creative agent to test different behavior.
root_agent = creative_agent

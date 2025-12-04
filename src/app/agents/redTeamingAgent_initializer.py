# Azure imports
from azure.identity import DefaultAzureCredential
from azure.ai.evaluation.red_team import RedTeam, RiskCategory, AttackStrategy
from pyrit.prompt_target import OpenAIChatTarget
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

# Azure AI Project Information
azure_ai_project = os.getenv("AZURE_AI_AGENT_ENDPOINT")

# Instantiate your AI Red Teaming Agent
red_team_agent = RedTeam(
    azure_ai_project=azure_ai_project,
    credential=DefaultAzureCredential(),
    risk_categories=[
        RiskCategory.Violence,
        RiskCategory.HateUnfairness,
        RiskCategory.Sexual,
        RiskCategory.SelfHarm
    ],
    num_objectives=5,
)

# Configuration for Azure OpenAI model
deployment_name = os.environ.get("gpt_deployment")
base_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
azure_endpoint = f"{base_endpoint.rstrip('/')}/openai/deployments/{deployment_name}/chat/completions"

azure_openai_config = {
    "azure_endpoint": azure_endpoint,
    "api_key": os.environ.get("AZURE_OPENAI_KEY"),
    "azure_deployment": deployment_name,
    "api_version": os.environ.get("AZURE_OPENAI_API_VERSION"),
}

async def main():
    red_team_result = await red_team_agent.scan(target=azure_openai_config)

asyncio.run(main())


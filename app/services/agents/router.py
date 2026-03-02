from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from app.core.config import settings

# Initialize the primary fast LLM
llm = ChatOpenAI(
    model="arcee-ai/trinity-large-preview:free", 
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0.0,
    max_retries=3
)

class RouteQuery(BaseModel):
    """Super Agent routing decision model."""
    intent: Literal["CASUAL", "COMPANY", "USER", "VESSEL", "DEFECT", "OUT_OF_SCOPE"] = Field(
        ...,
        description="Classify the user intent into one of the specialized domains, casual chatter, or out of scope."
    )

parser = JsonOutputParser(pydantic_object=RouteQuery)

system_prompt = """You are the Super Agent (Router) for the PulseMarine application.
Route the user's input to the correct expert database agent.

CRITICAL INSTRUCTION FOR FOLLOW-UPS:
If the user's input sounds like a correction or a piece of a previous context (e.g., "No, the vessel assigned to marine@yopmail.com", "What about defect 102?", "Count the companies"), you MUST route it to the corresponding domain agent based on the keywords. 
If the text contains the keywords "vessel", "company", "defect", or "user", heavily bias your routing to that domain. DO NOT default to OUT_OF_SCOPE for follow-up corrections.

Domains:
- CASUAL: STRICTLY ONLY Greetings, small talk, and pleasantries ("Hi", "How are you", "Thank you"). 
- COMPANY: Anything regarding companies, charterers, fleets, tags, or company emails/IDs.
- USER: Anything regarding users, admins, notifications, roles, or user emails.
- VESSEL: Anything regarding vessels, IMO numbers, vessel names, or vessel assignments.
- DEFECT: Anything regarding defects, severity, status, repair categories, or defect history.
- OUT_OF_SCOPE: General knowledge, math problems, writing code outside of PulseMarine, or completely irrelevant topics NOT related to maritime operations.

Rule: Output ONLY a valid JSON.
{format_instructions}
"""

router_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{question}")
]).partial(format_instructions=parser.get_format_instructions())

# Build the Langchain sequence using the JSON parser instead of tools
intent_router = router_prompt | llm | parser

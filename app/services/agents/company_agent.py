import re
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from app.core.config import settings
from app.services.prisma_executor import execute_prisma_code
from app.db.prisma_client import prisma_db

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0.0,
    max_retries=3
)

from app.services.agents.shared_schema import unified_schema

system_prompt = """You are a Prisma Python ORM expert.
Generate a valid Python asynchronous snippet using the Prisma client to answer the user's question.
You have access to the `db` variable (which is an initialized `Prisma()` client).
Your code must assign the final fetched data to a top-level variable named `result`.

Example:
```python
result = await db.company.find_many(where={{"name": "Tyco"}})
```

Prisma Schema Available:
{schema}

Rule: Output ONLY the valid Python code block. No explanations."""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{question}")
])

prisma_chain = prompt | llm

async def run_company_agent(query: str) -> str:
    """Generates Prisma code and executes it."""
    try:
        response = await prisma_chain.ainvoke({"question": query, "schema": unified_schema})
        raw_output = await execute_prisma_code(response.content, prisma_db)
        return str(raw_output)
    except Exception as e:
        return f"Error executing Company Prisma logic: {str(e)}"

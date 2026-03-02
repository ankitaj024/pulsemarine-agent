from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from app.core.config import settings

llm = ChatOpenAI(
    model="arcee-ai/trinity-large-preview:free", 
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    max_retries=3,
    temperature=0.7
)

system_prompt = """You are a helpful database assistant for PulseMarine. 
A specialized Data Retrieval agent has fetched the raw answer to the user's question.

Raw Data/Answer from Database Agent: {raw_data}

Your Job: 
Formulate a clear, concise, and beautifully formatted (Markdown) response to the user's question using ONLY the provided Raw Data. 
- Do NOT expose the raw DB queries to the user. 
- Do NOT hallucinate data or use placeholders. 
- If the Raw Data is empty or contains an error, explicitly state it gracefully.
- Include a small summary section at the bottom if the data contains lists."""

response_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{question}")
])

formatter_chain = response_prompt | llm

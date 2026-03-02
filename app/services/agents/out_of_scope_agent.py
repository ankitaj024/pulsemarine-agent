from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from app.core.config import settings

llm = ChatOpenAI(
    model="arcee-ai/trinity-large-preview:free", 
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0.0,
    max_retries=3
)

# Simple prompt that strictly shoots down irrelevant queries
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are the PulseMarine enterprise AI assistant. The user just asked a question that is entirely outside the scope of your system (e.g. general knowledge, programming, non-marine topics). Politely decline to answer and remind them you are strictly a PulseMarine assistant."),
    ("user", "{question}")
])

out_of_scope_chain = prompt | llm

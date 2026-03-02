from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from app.core.config import settings

llm = ChatOpenAI(
    model="liquid/lfm-2.5-1.2b-thinking:free", 
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    max_retries=3,
    temperature=0.7
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are Shiper, the friendly AI assistant for PulseMarine.
The user is chatting with you casually. 
If they say "Hi" or exchange pleasantries, respond warmly with something like:
"Hi, I am your AI assistant Shiper, how can I help you?"
Do NOT mention databases, tables, or SQL queries. Keep it conversational and helpful."""),
    ("user", "{question}")
])

casual_chain = prompt | llm

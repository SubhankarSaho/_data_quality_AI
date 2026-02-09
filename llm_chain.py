from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import GROQ_API_KEY

# Initialize Groq LLM
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.1-8b-instant",
    temperature=0.2
)

# Prompt template
prompt = ChatPromptTemplate.from_template("""
You are a senior data reliability engineer.

A metric anomaly was detected.

Metric ID: {metric}
Current Value: {value}
Z-score: {z_score}

Explain the MOST LIKELY root cause in simple business language.
If uncertainty exists, clearly state it.
""")

# LangChain Runnable
chain = prompt | llm | StrOutputParser()

def generate_explanation(metric: str, value: float, z_score: float) -> str:
    return chain.invoke({
        "metric": metric,
        "value": value,
        "z_score": z_score
    })

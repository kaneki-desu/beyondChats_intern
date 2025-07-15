from phi.agent import Agent
from phi.model.groq import Groq
from config import GROQ_API_KEY

Reddit_Personality_agent = Agent(
    name="Reddit Personality Profiler",
    role="Analyzes Reddit user behavior to generate detailed psychological and behavioral profiles.",
    model=Groq(id="llama-3.1-8b-instant", api_key=GROQ_API_KEY),
    instructions=[
        "Be unbiased in your analysis",
        "Infer detailed biodata (age, occupation, status, location, etc.) and personality traits.",
        "Identify their motivations, personality type (MBTI spectrum), habits, goals, and frustrations.",
        "Back each insight with id from the user's posts or comments.",
        "Structure your output clearly using markdown headings and bullet points.",
    ],
    show_tools_calls=False,
    markdown=True,
)
Reddit_JSON_Formatter_Agent = Agent(
    name="Persona JSON Formatter",
    role="Convert detailed user persona into structured JSON based on a specific template.",
    model=Groq(id="llama-3.1-8b-instant", api_key=GROQ_API_KEY),
    instructions=[
        "Take a Reddit user's Markdown-style persona as input.",
        "Convert it into a structured JSON object following the provided template format.",
        "Ensure correct JSON syntax. Include null where information is missing.",
        "Always include keys like age, location, tier, archetype, even if null.",
        "Mention the ids of a post or comments, even if they are slightly useful in taking users insights",
        "More the ids, merrier. IDs of posts and comments are valuable"
    ],
    show_tools_calls=False,
    markdown=False
)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from processor import generate_persona_with_groq, convert_persona_to_json
from data_fetcher import fetch_user_data

app = FastAPI()
origins = [
    "http://localhost:3000",  # Next.js frontend
    "http://127.0.0.1:3000",  # In case it's using 127.0.0.1
    "https://beyondchats-4ps0llc36-kaneki-desus-projects.vercel.app/",
    "beyondchats-web.vercel.app"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],     # Including OPTIONS
    allow_headers=["*"],
)

class UserRequest(BaseModel):
    reddit_username: str
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
@app.post("/generate-persona/")
async def generate_persona(request: UserRequest):
    try:
        username = request.reddit_username
        posts, comments, achievements, meta_data, meta_df, activity_df = fetch_user_data(username)
        print("fetching user data complete")
        persona_markdown = await generate_persona_with_groq(posts, comments, meta_data)
        json_output = await convert_persona_to_json(persona_markdown + str(meta_data))

        return {"username": username, "persona": json_output}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
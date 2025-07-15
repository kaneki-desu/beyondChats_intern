from processor import generate_persona_with_groq, convert_persona_to_json
from data_fetcher import fetch_user_data
import asyncio
url = "https://www.reddit.com/user/kojied/"
username = url.rstrip("/").split("/")[-1]

async def main(username):   
    posts, comments, achievements ,meta_data, meta_df , activity_df=fetch_user_data(username)
    persona =await generate_persona_with_groq(posts, comments,meta_data)
    json_persona= await convert_persona_to_json(persona+ meta_data)
    with open(f"{username}_persona.txt", "w", encoding="utf-8") as f:
        f.write("=== Persona ===\n")
        f.write(persona.strip() + "\n\n")
        f.write("=== JSON Persona ===\n")
        f.write(json_persona.strip())
    print(f"Saved to {username}_persona.txt")

if __name__ == "__main__":
    asyncio.run(main(username))
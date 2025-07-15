from processor import generate_persona_with_groq, convert_persona_to_json
from data_fetcher import fetch_user_data
import asyncio
url = "https://www.reddit.com/user/kojied/"
username = url.rstrip("/").split("/")[-1]

async def main(username):   
    posts, comments, achievements , meta_df , activity_df= fetch_user_data(username)
    persona =await generate_persona_with_groq(posts, comments)
    json_persona= await convert_persona_to_json(persona)
    print(json_persona)

if __name__ == "__main__":
    asyncio.run(main("Hungry-move-6603"))
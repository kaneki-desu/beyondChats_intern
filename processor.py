import tiktoken
from agents import Reddit_JSON_Formatter_Agent, Reddit_Personality_agent

# Helper to count tokens
def count_tokens(text, model="gpt-3.5-turbo"):
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))
def split_into_chunks(posts, comments, max_chunk_tokens=5500):
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")  # still fine for LLaMA approximation
    full_text = f"POSTS:\n{posts}\nCOMMENTS:\n{comments}"
    tokens = enc.encode(full_text)

    chunks = []
    for i in range(0, len(tokens), max_chunk_tokens):
        chunk_tokens = tokens[i:i + max_chunk_tokens]
        chunk_text = enc.decode(chunk_tokens)
        chunks.append(chunk_text)

    print(f"[DEBUG] Total chunks formed: {len(chunks)}")
    return chunks

# Generate persona in chunks
async def generate_persona_with_groq(posts, comments,meta_data):
    chunks = split_into_chunks(posts, comments)
    full_persona = ""
    for i, chunk in enumerate(chunks):
        prompt = f"""
        You are an expert personality analyst bot. Give detailed analysis take your time.
        Given the Reddit user's posts/comments chunk below, extract relevant personality insights.
        Look into matter about the created_utc, the subreddit 
        Pass the id of any record that support maybe a little bit of insights.
        Mention atleast 5 ids or more.
        Use of fractions is preffered rather than high, moderate etc.
        CHUNK {i+1}/{len(chunks)}:
        {chunk}
        """
        print(f"[+] Processing chunk {i+1}/{len(chunks)}")
        response = await Reddit_Personality_agent.arun(prompt)
        full_persona += f"\n\n### Chunk {i+1} Analysis\n{response.content}"
    
    final_prompt =  f"""You are an expert personality analyst bot. Analyse the chunks and give me a very detailed report for each of the sections listed below.
        Given the Reddit user's meta data of the account ,comments and posts below, extract a detailed **User Persona** including:
        1.Biodata such as AGE, Occupation, Status, Location, TIER, ARCHETYPE, behavior(such as Practical, Adaptable, Spontaneuos, Active)
        2.Motivations (such as Convenience level, wellness level, speed level, preferences level, comfort levvel, Dietary needs level)
        3.Personality (Introvert to extrovert, intuition to sensing, feeling to thinking, perceiving to judging)
        4.Behaviour & habits
        5. Goals & Needs,
        6.Frustations
        For **each point**, cite id from the user’s posts/comments that support it.Mention more ids, as much as possible.Mention atleast 10-20 ids
        ### Metadata:{meta_data}
        The insights taken from previous passed chunks are:{full_persona}"""
    print("[+] Generating user persona...")
    Users_Info = await Reddit_Personality_agent.arun(final_prompt)
    return Users_Info.content
async def convert_persona_to_json(markdown_persona: str):
    json_prompt = """
    You will be given a user persona written in markdown with section headings such as Biodata, Motivations, Personality, etc.
    In "AI_insigts", you explain how you got the corresponding attributes details and they must contain ids of those posts or comments.
    Each AI_insights must be back by the post id's . If you are guessing some attributes , write how you guessed it in AI_insights if possible with ids.
    You can add new attributes in personality , motivation.
    Please double-check each word , each commas, each bracket ,each literals and characters before giving the final output as it gets difficult to debug in frontend
    Example template:
    {
      "persona": {
        "reddit_username": "Abcd",
        "name": "Lucas Mellor",
        "photo_url": "",
        "demographics": {
          "age": null,
          "occupation": "Content Manager",
          "location": "London, UK",
          "Marital_Status": "Single",
          "Tier": "Early Adopters",
          "archetype": "The Creator",
          "AI_insights": "In Comment id='t1_mvt4t5c', Lucas mentioned managing a content calendar and writing for digital platforms, suggesting his role as a Content Manager. In Post id='t3_j9x4z2', he shared a photo of his neighborhood in London and referenced commuting pre-lockdown."
        },
        "quote": "I want to spend less time ordering a healthy takeaway and more time enjoying my meal.",
        "traits": {
          "content": ["Practical", "Adaptable", "Spontaneous", "Active"],
          "AI_insights": "These traits are inferred from Post id='t3_j9fdg1' where Lucas shares how he adapted to a healthier lifestyle with HIIT. His spontaneity is seen in Comment id='t1_mvu6n4k' when he mentions randomly trying a new cuisine."
        },
        "motivations": {
          "content": [
            {"Convienience": 0.85},
            {"Wellness": 0.80},
            {"Speed": 0.75},
            {"Preference": 0.35},
            {"Comfort": 0.50},
            {"Dietary Needs": 0.95}
          ],
          "AI_insights": "Post id='t3_j9fdg1' discusses Lucas wanting healthy meals that are quick to order. Comment id='t1_mvti9qp' highlights his concern over ingredients due to dietary restrictions."
        },
        "personality": {
          "content": [
            {
              "spectrum_low": "Introvert",
              "spectrum_high": "Extrovert",
              "fraction_high": 0.80
            },
            {
              "spectrum_low": "Intuition",
              "spectrum_high": "Sensing",
              "fraction_high": 0.85
            },
            {
              "spectrum_low": "Feeling",
              "spectrum_high": "Thinking",
              "fraction_high": 0.75
            },
            {
              "spectrum_low": "Perceiving",
              "spectrum_high": "Judging",
              "fraction_high": 0.15
            }
          ],
          "AI_insights": "Lucas exhibits extroverted and sensing tendencies based on Comment id='t1_mvtf0u2' where he talks about leading team Zoom calls and reacting based on daily events. His logical analysis of menu options in t1_mvtr2kl implies a thinking-over-feeling tendency."
        },
        "behaviors_habits": {
          "content": [
            "Lucas usually had meals before the lockdown, as he wasn't keen on cooking. He relied on ready meals and takeaways.",
            "He is technology savvy and has ordered all his meals exclusively online in the comfort of his home.",
            "During the lockdown, he began taking part in online HIIT exercise sessions and started to implement changes to enjoy a healthier lifestyle.",
            "Lucas works from home during the lockdown and finds it hard to balance work and his newfound healthy lifestyle.",
            "He orders a takeaway at least 3 times a week, and is always looking for new healthy options."
          ],
          "AI_insights": "Comments id='t1_mvtg2qf', t1_mvth1xn, and Post id='t3_j9z9mx' refer to Lucas' home-based lifestyle, online workouts, and reliance on food delivery platforms like UberEats and Deliveroo."
        },
        "goals_needs": {
          "content": [
            "To enjoy a healthy diet and lifestyle during lockdown",
            "To help all the information, he needs to select a healthy takeaway meal"
          ],
          "AI_insights": "Comment id='t1_mvth9ax' clearly states 'I’m trying to eat better but it's hard to tell which takeout is actually healthy.' Post id='t3_j9z1b8' includes his weekly HIIT tracking goal."
        },
        "pain_points": {
          "content": [
            "Wasting time Googling menu items because of lack of images or description",
            "Can't find a category for healthy meals on the cuisine section",
            "Pain point #2"
          ],
          "AI_insights": "Comment id='t1_mvtk6d3' says 'Why do half the menus have no pics? I end up Googling half the items!' and id='t1_mvtl9sn' states 'Wish there was just a Healthy tab instead of guessing by name.'"
        },
        "tools_technology": {
          "content": [
            "Tool or tech #1",
            "Tool or tech #2"
          ],
          "AI_insights": "Lucas mentioned using apps like MyFitnessPal (Comment id='t1_mvtqd1n') and Fitbit (Comment id='t1_mvtqxe7') to track meals and exercise."
        }
      }
    }

    Use the following format as a schema:

    #json
    {{
      "persona": {{
        "reddit_username": "{username}",
        "name": null,
        "photo_url": "",
        "demographics": {{
          "age": null,
          "occupation": null,
          "location": null,
          "marital_status": null,
          "tier": null,
          "archetype": null,
          "AI_insights": ""
        }},
        "quote": "",
        "traits": {{
          "content": [],
          "AI_insights": ""
        }},
        "motivations": {{
          "content": [],
          "AI_insights": ""
        }},
        "personality": {{
          "content": [],
          "AI_insights": ""
        }},
        "behaviors_habits": {{
          "content": [],
          "AI_insights": ""
        }},
        "goals_needs": {{
          "content": [],
          "AI_insights": ""
        }},
        "pain_points": {{
          "content": [],
          "AI_insights": ""
        }},
        "tools_technology": {{
          "content": [],
          "AI_insights": ""
        }}
      }}
    }}

    Here is the input persona:"""+markdown_persona+"""Return **only** the JSON."""
    print("[+] Converting persona markdown to JSON...")
    result = await Reddit_JSON_Formatter_Agent.arun(json_prompt)
    return result.content

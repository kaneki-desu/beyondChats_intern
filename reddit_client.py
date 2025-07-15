import praw
from config import REDDIT_CLIENT_ID, REDDIT_SECRET

reddit =praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_SECRET,
    user_agent="persona_extractor by u/yourusername"
)

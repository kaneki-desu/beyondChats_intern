import pandas as pd
from datetime import datetime
from reddit_client import reddit
def fetch_user_metadata(user):
    metadata = {
        "username": user.name,
        "is_employee": user.is_employee,
        "is_mod": user.is_mod,
        "has_verified_email": user.has_verified_email,
        "created_utc": datetime.utcfromtimestamp(user.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
        "link_karma": user.link_karma,
        "comment_karma": user.comment_karma,
        "total_karma": user.link_karma + user.comment_karma,
        "subreddit_title": getattr(user.subreddit, 'title', None),
        "subreddit_public_description": getattr(user.subreddit, 'public_description', None),
        "subreddit_description": getattr(user.subreddit, 'description', None),
        "trophies": ", ".join([t.name for t in user.trophies()])
    }
    return metadata
def fetch_user_posts(user, limit=150):
    posts_data = []
    for post in user.submissions.new(limit=limit):
        posts_data.append({
            "type": "post",
            "id": post.id,
            "created_utc": datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
            "title": post.title,
            "text": post.selftext,
            "score": post.score,
            "subreddit": post.subreddit.display_name,
            "url": post.url
        })
    return posts_data
def fetch_user_comments(user, limit=100):
    comments_data = []
    for comment in user.comments.new(limit=limit):
        comments_data.append({
            "type": "comment",
            "id": comment.id,
            "created_utc": datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
            "text": comment.body,
            "score": comment.score,
            "subreddit": comment.subreddit.display_name,
            "link_id": comment.link_id
        })
    return comments_data
def fetch_user_dataframes(username):
    user = reddit.redditor(username)
    metadata = fetch_user_metadata(user)
    posts = fetch_user_posts(user)
    comments = fetch_user_comments(user)
    meta_df = pd.DataFrame([metadata])
    activity_df = pd.DataFrame(posts + comments)
    
    return meta_df, activity_df
def fetch_user_data(username):
    meta_df, activity_df = fetch_user_dataframes(username)
    meta_df = meta_df.sort_values(by='created_utc', ascending=True)
    activity_df = activity_df.sort_values(by='created_utc', ascending=True)
    posts = activity_df[activity_df['type'] == 'post'].to_dict(orient='records')
    comments = activity_df[activity_df['type'] == 'comment'].to_dict(orient='records')
    achievements = activity_df[activity_df['type'] == 'achievement']['title'].tolist()
    meta_data = str(meta_df.to_dict(orient='records')[0])
    return posts, comments, achievements,meta_data, meta_df , activity_df

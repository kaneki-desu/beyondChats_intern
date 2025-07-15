# 2ndApproach: Advanced Reddit User Profiling via Topic Modeling & Trait Extraction

This approach leverages topic modeling, sentiment analysis, emotion detection, and behavioral trait extraction to build a comprehensive Reddit user profile. The workflow is implemented in the `TopicModeling.ipynb` notebook and produces both qualitative and quantitative persona reports.
This approach has seen all the records instead of the main approach where only due to Rate Limit we were unable to get information from all the posts and comments till date uploaded by the user.

## Key Steps
1. **Data Collection**
   - Fetch Reddit user posts and comments using PRAW and custom fetchers.
   - Save activity data to CSV for further analysis.

2. **Preprocessing & Enrichment**
   - Clean and combine post/comment text.
   - Tokenize and remove stopwords.
   - Enrich data with sentiment scores (VADER), toxicity (Detoxify), and emotion (NRCLex).

3. **Topic Modeling**
   - Use BERTopic to extract dominant topics from user content.
   - Save topic insights and representative examples.

4. **Trait & Behavior Analysis**
   - Calculate Big Five (OCEAN) trait scores from word frequencies.
   - Estimate MBTI type using keyword patterns.
   - Categorize behaviors (work, home, entertainment, social, health, etc.) and normalize frequencies.

5. **Persona Report Generation**
   - Save qualitative persona, topic insights, and behavioral profiles to text files.
   - Combine all reports into a single user profile file.

6. **JSON Conversion**
   - Use an LLM agent to convert the combined profile into a structured JSON persona for downstream use.

## How to Use
Step 1: py -3.10 -m venv env 
Step 2:pip install -r TopicModeling_req.txt
Step 3: Make a .env file like the sample
Step 4:- Run the cells in `TopicModeling.ipynb` sequentially to:
        - Fetch and preprocess Reddit data
        - Perform sentiment, emotion, and topic analysis
        - Extract behavioral traits and generate reports
        - Combine and convert the profile to JSON
(You may need to install additional modules)
## Output Files
- `UserProfile/qualitative_persona.txt`: Qualitative summary of user traits and background
- `UserProfile/persona_profile.txt`: Sentiment, emotion, and topic insights
- `UserProfile/behavior_profile.txt`: Behavioral category analysis
- `UserProfile/combined_user_profile.txt`: Merged profile for JSON conversion

## Notes
- This approach is modular and extensible for additional traits or data sources.
- The final JSON persona is suitable for integration with other systems or for frontend display.

## Requirements
- Python packages: pandas, nltk, detoxify, nrclex, bertopic, praw
- Reddit API credentials in your environment

## License
MIT License

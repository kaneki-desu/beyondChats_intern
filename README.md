# Reddit Personality Profiler

This project analyzes Reddit user behavior to generate detailed psychological and behavioral profiles, and formats them into structured JSON. It uses FastAPI for deployment and also supports local persona storage as {username}_persona.txt.

## Features
- Fetches Reddit user posts, comments, and metadata
- Generates a detailed persona using Agentic AI (Phidata and Groq API)
- Converts persona to structured JSON format
- Local text storage of persona and JSON
- FastAPI backend for deployment and API access

## Project Structure
- `main2.py`: Run this script for local persona extraction and to save results as a text file. Useful for testing and offline analysis.
- `main.py`: FastAPI application for deployment. Provides an API endpoint to generate and retrieve Reddit user personas.
- `agents.py`: Defines LLM agents for persona analysis and JSON formatting.
- `processor.py`: Handles persona generation and formatting logic.
- `data_fetcher.py`: Fetches Reddit user data.
- `reddit_client.py`: Reddit API client setup.
- `config.py`: Configuration and environment variables.
- `requirements.txt`: Python dependencies for deployment and development.
- `scraping_requirements.txt`: Additional dependencies for scraping tasks.
- `Data/`: Example data and persona files.

## Usage

### Local Persona Extraction
To extract and save a Reddit user's persona locally:
```bash
python main2.py
```
This will create a text file with the persona and its JSON representation.

### API Deployment
To deploy the FastAPI backend:
```bash
python main.py
```
Access the API at `http://127.0.0.1:8000`.

## Environment Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up your `.env` file with the following variables:
   - `REDDIT_CLIENT_ID`
   - `REDDIT_SECRET`
   - `GROQ_API_KEY`
REDDIT_CLIENT_ID:Get this from Reddit's Developer Portal. It uniquely identifies your Reddit app.
REDDIT_SECRET:This is the secret key that Reddit gives you alongside your client ID. 
GROQ_API_KEY:This is your API key for using the Groq API. It allows you to access their LLMs like LLaMA-3 for personality analysis.

## Notes
- Use `main2.py` for local text storage and persona extraction.
- Use `main.py` for API deployment and integration with frontend applications.

## License
MIT License

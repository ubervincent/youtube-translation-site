from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
load_dotenv()

def get_transcript_by_url(url: str) -> str:
    video_id = url.split('=')[1].split('&')[0]
    print(f"Video ID: {video_id}")
    return YouTubeTranscriptApi.get_transcript(video_id)

def convert_timestamped_transcript_to_text(timestamped_transcript: list[dict]) -> str:
    return ' '.join([item['text'] for item in timestamped_transcript])

translation_prompt = """
You are a helpful assistant that translate transcript of YouTube videos in English to Traditional Cantonese. Make sure the translation is accurate and easy to understand.
"""

def translate_text(timestamped_transcript: list[dict]) -> str:
    transcript = convert_timestamped_transcript_to_text(timestamped_transcript)

    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": translation_prompt},
            {"role": "user", "content": transcript}
        ],
    )
    
    return response.choices[0].message.content
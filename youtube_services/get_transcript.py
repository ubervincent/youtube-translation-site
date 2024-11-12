from utils.utils import write_content_to_file
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()


def get_transcript_by_url(url: str) -> str:
    video_id = url.split('=')[1].split('&')[0]
    
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    write_content_to_file(
        output_path='./transcripts',
        content=transcript,
        filename=f'{video_id}.txt'
    )

    return transcript

def convert_timestamped_transcript_to_text(timestamped_transcript: list[dict]) -> str:
    return ' '.join([item['text'] for item in timestamped_transcript])

target_language = "Traditional Cantonese"

translation_prompt = f"""
You are a helpful assistant that translate transcript of YouTube videos in English to {target_language}. 
Make sure the translation is easy to understand for my parents who's learning English as a second language.
Add the html line breaks symbol <br> between each sentence so that the translation can be read line by line for HTML display.
"""

def translate_text(timestamped_transcript: list[dict]) -> str:
    transcript = convert_timestamped_transcript_to_text(timestamped_transcript)

    print(f"Transcript: {transcript}")

    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": translation_prompt},
            {"role": "user", "content": transcript}
        ],
    )
    
    return response.choices[0].message.content
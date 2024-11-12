from utils.utils import write_content_to_file, get_video_id_from_url, read_content_from_file
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
from dotenv import load_dotenv

import os
load_dotenv()


def get_transcript_by_url(url: str) -> str:
    video_id = get_video_id_from_url(url)
    
    payload = {
        'transcript': None,
        'video_id': video_id
    }
    
    # if check_if_video_has_been_translated(video_id):
    #     payload['transcript'] = return_translation_data(video_id)
    #     return payload
    
    # else:
    transcript = YouTubeTranscriptApi.get_transcript(video_id, proxies={"http": f"http://oiholelg-rotate:h3zcpwb3wbr7@p.webshare.io:80/"})

    write_content_to_file(
        output_path='./transcripts',
        content=transcript,
        filename=f'{video_id}.json'
    )
    payload['transcript'] = transcript
    return payload

def convert_timestamped_transcript_to_text(timestamped_transcript: list[dict]) -> str:
    return ' '.join([item['text'] for item in timestamped_transcript])

def get_translation_prompt(transcript: str) -> str:
    
    target_language = "Traditional Cantonese"

    translation_prompt = f"""
    You are a helpful assistant that translate transcript of YouTube videos in English to {target_language}. 
    Make sure the translation is easy to understand for my parents who's learning English as a second language.
    Add line breaks symbol <br> between each sentence, and tag each sentence with <p> tags so that the translation can be read line by line.
    """

    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": translation_prompt},
            {"role": "user", "content": transcript}
        ],
    )

    return response.choices[0].message.content

def translate_text(transcript_data: dict) -> str:
    if check_if_video_has_been_translated(transcript_data['video_id']):
        return return_translation_data(transcript_data['video_id'])
    
    else:
        # convert the transcript to a string
        transcript = convert_timestamped_transcript_to_text(transcript_data['transcript'])
    
        # get the translation
        translation = get_translation_prompt(transcript)
        
        # write the translation to a file
        write_content_to_file(
            output_path='./translations',
            content=translation,
            filename=f'{transcript_data["video_id"]}.txt'
        )
    
        return translation

def check_if_video_has_been_translated(video_id: str) -> bool:
    return os.path.exists(f'./translations/{video_id}.txt')

def return_translation_data(video_id: str) -> dict:
    return read_content_from_file(f'./translations/{video_id}.txt')
    
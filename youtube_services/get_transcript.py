from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript_by_url(url: str) -> str:
    video_id = url.split('=')[1].split('&')[0]
    print(f"Video ID: {video_id}")
    return YouTubeTranscriptApi.get_transcript(video_id)


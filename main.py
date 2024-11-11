import argparse
from youtube_services.get_transcript import get_transcript_by_url
# Create argument parser
parser = argparse.ArgumentParser(description='Download YouTube videos using yt-dlp')
parser.add_argument('url', help='YouTube video URL to download')

# Parse arguments
args = parser.parse_args()

try:
    transcript = get_transcript_by_url(args.url)
    print(f"Transcript: {transcript}")
except Exception as e:
    print(f"Error: {str(e)}")
    exit(1) 
import subprocess
from typing import Optional
from pathlib import Path
import argparse
import logging

def download_youtube_video(url: str, output_path: Optional[str] = None) -> str:
    """Download a YouTube video using yt-dlp command line tool and return its file path."""
    if not url:
        raise ValueError("URL cannot be empty")
        
    output_dir = Path(output_path) if output_path else Path.cwd()
    output_template = str(output_dir / '%(title)s.%(ext)s')
    
    # Construct the yt-dlp command
    command = [
        'yt-dlp',
        '--format', 'mp4/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        '--output', output_template,
        '--quiet',
        url
    ]
    
    try:
        # Run the command and capture output
        result = subprocess.run(command, 
                              capture_output=True, 
                              text=True, 
                              check=True)
        
        # The actual filename will be in the last line of stdout
        if result.stdout:
            return result.stdout.strip().split('\n')[-1]
        else:
            raise Exception("No output file path returned")
            
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to download video: {e.stderr}")
    except Exception as e:
        raise Exception(f"Error during download: {str(e)}")

# Usage
if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description='Download YouTube videos using yt-dlp')
    parser.add_argument('url', help='YouTube video URL to download')
    parser.add_argument('--output', '-o', 
                       help='Output directory (optional)',
                       default=None)
    
    # Parse arguments
    args = parser.parse_args()
    
    try:
        video_path = download_youtube_video(args.url, args.output)
        print(f"Video downloaded to: {video_path}")
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1) 
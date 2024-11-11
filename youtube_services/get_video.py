import subprocess
import os

def download_youtube_video(url: str) -> str:
    """Download a YouTube video using yt-dlp command line tool and return its file path."""
    if not url:
        raise ValueError("URL cannot be empty")
        
    output_dir = "./videos"
    output_template = os.path.join(output_dir, '%(title)s.%(ext)s')
    
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
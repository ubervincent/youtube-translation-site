from pytube import YouTube

def download_youtube_video(url: str, output_path: str = "downloads") -> str:
    """Download a YouTube video and return its file path."""
    try:
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').first()
        return video.download(output_path=output_path)
    except Exception as e:
        raise Exception(f"Failed to download video: {str(e)}")

# Usage
if __name__ == "__main__":
    try:
        video_path = download_youtube_video("https://www.youtube.com/watch?v=your_video_id")
        print(f"Video downloaded to: {video_path}")
    except Exception as e:
        print(f"Error: {str(e)}") 
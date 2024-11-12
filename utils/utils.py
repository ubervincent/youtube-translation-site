import logging
from pathlib import Path
from typing import Union
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def write_content_to_file(
    output_path: str,
    content: Union[str, dict],
    filename: str
) -> Path:
    """
    Write content to a file in the specified output path.
    
    Args:
        output_path: Directory path where file should be saved
        content: Content to write (string or dictionary)
        filename: Name of the file to create
        
    Returns:
        Path: Path object pointing to the created file
        
    Raises:
        IOError: If directory creation or file writing fails
    """
    try:
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        file_path = output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            if isinstance(content, dict):
                json.dump(content, f, ensure_ascii=False, indent=2)
            else:
                f.write(str(content))
                
        logger.info(f"Successfully wrote content to {file_path}")
        return file_path
        
    except Exception as e:
        logger.error(f"Failed to write content to {filename}: {str(e)}")
        raise IOError(f"Failed to write file: {str(e)}")

def read_content_from_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if file_path.endswith('.json'):
            return json.loads(content)
        else:
            return content
    
def get_video_id_from_url(url: str) -> str:
    import re
    match = re.search(r'[a-zA-Z0-9]{10,14}', url)
    if match:
        return match.group(0)
    else:
        raise ValueError("Video ID not found in URL")

def get_embed_url_from_video_id(video_id: str) -> str:
    return f"https://www.youtube.com/embed/{video_id}"
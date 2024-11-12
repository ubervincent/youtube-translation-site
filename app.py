from flask import Flask, render_template, request, jsonify
from markupsafe import Markup
from youtube_services.get_transcript import get_transcript_by_url, convert_timestamped_transcript_to_text, translate_text
from utils.utils import get_video_id_from_url, get_embed_url_from_video_id
import logging

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='app.log',
                    filemode='w')

logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='site')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate')
def translate():
    data = request.args
    url = data.get('video-url')
    
    video_id = get_video_id_from_url(url)
    embed_url = get_embed_url_from_video_id(video_id)    

    translated_transcript = translate_text(get_transcript_by_url(url))
    
    return render_template('index.html', video_id=video_id, embed_url=embed_url, translated_transcript=Markup(translated_transcript))

if __name__ == '__main__':
    logger.info('Starting Flask app')
    app.run(debug=True, port=8000, host='0.0.0.0') 
from flask import Flask, render_template, request, jsonify
from youtube_services.get_transcript import get_transcript_by_url, convert_timestamped_transcript_to_text, translate_text

app = Flask(__name__, template_folder='site')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    url = data.get('url')
    translated_transcript = translate_text(get_transcript_by_url(url))
    return jsonify({'transcript': translated_transcript})

if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0') 
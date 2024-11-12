from flask import Flask, render_template, request, jsonify
from youtube_services.get_transcript import get_transcript_by_url

app = Flask(__name__, template_folder='site')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    url = data.get('url')
    transcript = get_transcript_by_url(url)
    return jsonify({'transcript': transcript})

if __name__ == '__main__':
    app.run(debug=True, port=5000) 
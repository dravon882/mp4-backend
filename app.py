from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)  # allow cross-origin from your frontend

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        # collect mp4 formats
        formats = []
        for f in info.get('formats', []):
            if f.get('url') and f.get('ext') in ('mp4', 'm4a', 'webm'):
                formats.append({
                    'format_id': f.get('format_id'),
                    'quality': f.get('format_note') or f.get('resolution') or f.get('height'),
                    'ext': f.get('ext'),
                    'url': f.get('url'),
                    'filesize': f.get('filesize') or f.get('filesize_approx')
                })

        return jsonify({
            'title': info.get('title'),
            'thumbnail': info.get('thumbnail'),
            'formats': formats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return "MP4 Download API running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

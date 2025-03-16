from flask import Flask, request, send_file
import requests
import os

app = Flask(__name__)

# Home Route
@app.route('/')
def home():
    return "Telegram PDF Downloader is Running!"

# PDF Download Route
@app.route('/download', methods=['GET'])
def download_pdf():
    file_url = request.args.get('url')  # PDF link from query parameter
    if not file_url:
        return "Please provide a valid URL!", 400

    response = requests.get(file_url)
    if response.status_code != 200:
        return "Failed to download the file!", 500

    file_path = "downloaded.pdf"
    with open(file_path, "wb") as file:
        file.write(response.content)

    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)